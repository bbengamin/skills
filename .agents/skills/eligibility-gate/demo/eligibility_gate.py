"""Eligibility gate: the deterministic per-person verdict for the outbound engine.

RL-428. Pure, dependency-free, read-only logic. NO Twenty access, NO network,
NO writes. The gate decides; callers (twenty-engine-sync, Apollo ingest, Clay
enrichment, campaign assembly) carry out the verdict.

The single rule the gate exists to enforce: a person flows through one ordered
decision and lands on exactly one verdict, the same way every run. Hard stops
are evaluated before any verdict that implies spending, so the gate never tells
a caller to re-enrich (a Clay credit cost) someone it would have suppressed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


# --------------------------------------------------------------------------- #
# Verdicts
# --------------------------------------------------------------------------- #

SUPPRESS = "suppress"      # policy-excluded from this campaign (not re-eligible)
SKIP = "skip"              # not actionable now, re-runnable later (cooldown / QA)
SOURCE = "source"          # net-new, eligible -> caller creates the record
RE_ENRICH = "re-enrich"    # matched, enrichment stale/missing -> caller refreshes
REUSE = "reuse"            # matched, enrichment fresh -> caller uses as-is

ACTIONABLE = (SOURCE, RE_ENRICH, REUSE)

# Identity resolution outcomes (owned by twenty-engine-sync / RL-439; consumed here)
MATCH = "match"
NO_MATCH = "no-match"
FUZZY_CANDIDATE = "fuzzy-candidate"
COLLISION = "collision"


# --------------------------------------------------------------------------- #
# Inputs (read-only views of golden-record + config state)
# --------------------------------------------------------------------------- #

@dataclass
class Person:
    id: str
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    name: str = ""
    lifecycle_stage: str = "lead"          # lead/contacted/.../customer/disqualified
    do_not_contact: bool = False
    last_enriched_at: Optional[str] = None  # ISO 8601
    # one-active-campaign pointer, resolved to the campaign the person is active in:
    active_campaign_id: Optional[str] = None
    # most recent campaignTouch.touchedAt across the person's memberships:
    latest_touch_at: Optional[str] = None   # ISO 8601
    # per (person x LinkedIn account) connection state on the target membership:
    connection_state: str = "NONE"          # NONE/PENDING/CONNECTED/WITHDRAWN/DECLINED


@dataclass
class EngineConfig:
    ttl_days: int = 90
    # channels the campaign runs, in priority order:
    campaign_channels: tuple = ("LINKEDIN", "EMAIL")
    # sending accounts available, by channel, that are ACTIVE and within dailyLimit:
    active_accounts: dict = field(default_factory=lambda: {"LINKEDIN": "li-acct-1",
                                                            "EMAIL": "em-acct-1"})
    blocklist_keys: frozenset = frozenset()  # normalized identity keys, hard-excluded


@dataclass
class GateInput:
    outcome: str                  # MATCH / NO_MATCH / FUZZY_CANDIDATE / COLLISION
    campaign_id: str
    person: Optional[Person] = None
    now: str = "2026-06-25T00:00:00Z"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _parse(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


def _age_days(ts: Optional[str], now: str) -> Optional[float]:
    t = _parse(ts)
    if t is None:
        return None
    return (_parse(now) - t).total_seconds() / 86400.0


def _required_channel_key_missing(person: Person, channels) -> bool:
    """A channel the campaign uses has no usable identity key on the record."""
    if "EMAIL" in channels and not person.email:
        return True
    if "LINKEDIN" in channels and not person.linkedin_url:
        return True
    return False


def _route(person: Optional[Person], cfg: EngineConfig):
    """Connection-aware channel + sending-account hint. None when no open channel."""
    state = person.connection_state if person else "NONE"
    has_email = bool(person.email) if person else False

    def acct(ch):
        return cfg.active_accounts.get(ch)

    if "LINKEDIN" in cfg.campaign_channels and acct("LINKEDIN"):
        if state == "CONNECTED":
            return {"channel": "LINKEDIN", "action": "message", "account": acct("LINKEDIN")}
        if state in ("NONE", "PENDING"):
            return {"channel": "LINKEDIN", "action": "connection_request", "account": acct("LINKEDIN")}
        # WITHDRAWN / DECLINED -> do not re-attempt LinkedIn; fall through to email
    if "EMAIL" in cfg.campaign_channels and acct("EMAIL") and (has_email or person is None):
        return {"channel": "EMAIL", "action": "email", "account": acct("EMAIL")}
    return None


def _verdict(v, reason, routing=None):
    return {"verdict": v, "reason": reason, "routing": routing}


# --------------------------------------------------------------------------- #
# The gate
# --------------------------------------------------------------------------- #

def decide(gi: GateInput, cfg: EngineConfig) -> dict:
    """Return exactly one verdict + reason (+ routing for actionable verdicts).

    Order: identity -> hard suppression -> active-campaign suppression ->
    TTL cooldown -> data verdict -> connection-aware routing.
    """
    # 1. identity / dedup
    if gi.outcome in (FUZZY_CANDIDATE, COLLISION):
        return _verdict(SKIP, "awaiting-qa")
    net_new = gi.outcome == NO_MATCH
    person = None if net_new else gi.person
    if not net_new and person is None:
        raise ValueError("MATCH outcome requires a person")

    # 2. hard suppression (matched records only)
    if person is not None:
        keys = {k for k in (person.linkedin_url, person.email) if k}
        if person.do_not_contact:
            return _verdict(SUPPRESS, "do-not-contact")
        if person.lifecycle_stage.lower() == "customer":
            return _verdict(SUPPRESS, "existing-client")
        if keys & set(cfg.blocklist_keys):
            return _verdict(SUPPRESS, "blocklist")

        # 3. active-campaign suppression (one active campaign per person, global)
        if person.active_campaign_id and person.active_campaign_id != gi.campaign_id:
            return _verdict(SUPPRESS, "active-elsewhere")

        # 4. TTL / re-contact cooldown
        age = _age_days(person.latest_touch_at, gi.now)
        if age is not None and age < cfg.ttl_days:
            return _verdict(SKIP, f"within-cooldown:{cfg.ttl_days}d")

    # 6. routing (computed up front so a no-open-channel downgrades to skip)
    routing = _route(person, cfg)
    if routing is None:
        return _verdict(SKIP, "no-open-channel")

    # 5. data verdict for eligible people
    if net_new:
        return _verdict(SOURCE, "net-new", routing)
    stale = _age_days(person.last_enriched_at, gi.now)
    if (person.last_enriched_at is None
            or (stale is not None and stale >= cfg.ttl_days)
            or _required_channel_key_missing(person, cfg.campaign_channels)):
        return _verdict(RE_ENRICH, "stale-or-missing-key", routing)
    return _verdict(REUSE, "fresh", routing)


def decide_batch(inputs, cfg: EngineConfig):
    """Run the gate over a batch, returning a verdict row per input. Read-only."""
    return [(gi, decide(gi, cfg)) for gi in inputs]
