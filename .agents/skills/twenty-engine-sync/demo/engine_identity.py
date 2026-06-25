"""Identity resolution + golden-record merge for the outbound engine.

RL-427 wave (RL-439 resolver, RL-440 auto-merge/survivorship, RL-441 fuzzy QA).

Pure, dependency-free, read-only logic. NO Twenty access, NO network, NO writes.
Everything here operates on in-memory dictionaries so the behaviour can be
demonstrated on a synthetic sample. Twenty integration (find_many_people,
additive update-by-id) is the responsibility of the twenty-engine-sync caller;
this module only decides what *would* happen.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# --------------------------------------------------------------------------- #
# Key normalization
# --------------------------------------------------------------------------- #

def normalize_linkedin(url: Optional[str]) -> Optional[str]:
    """Normalize a LinkedIn profile URL to a stable comparison key.

    Lowercase, drop scheme/host/www, drop query+fragment, collapse the
    /in/<handle> path, strip a trailing slash. Returns None for empty input.
    """
    if not url:
        return None
    u = url.strip().lower()
    if not u:
        return None
    for prefix in ("https://", "http://"):
        if u.startswith(prefix):
            u = u[len(prefix):]
    if u.startswith("www."):
        u = u[4:]
    # strip host if a linkedin domain is present, keep the path
    for host in ("linkedin.com", "lnkd.in"):
        idx = u.find(host)
        if idx != -1:
            u = u[idx + len(host):]
            break
    u = u.split("?", 1)[0].split("#", 1)[0]
    u = u.strip("/")
    return u or None


def normalize_email(email: Optional[str]) -> Optional[str]:
    """Normalize an email to a stable comparison key (lowercase + trim).

    Plus-addressing and dotted gmail localparts are intentionally NOT folded:
    that is a lossy assumption and is left to a documented, opt-in rule so the
    resolver never silently treats two distinct mailboxes as one.
    """
    if not email:
        return None
    e = email.strip().lower()
    return e or None


def email_domain(email: Optional[str]) -> Optional[str]:
    e = normalize_email(email)
    if not e or "@" not in e:
        return None
    return e.split("@", 1)[1]


# --------------------------------------------------------------------------- #
# String similarity (fuzzy scoring, RL-441) -- stdlib only
# --------------------------------------------------------------------------- #

def _jaro(a: str, b: str) -> float:
    if a == b:
        return 1.0
    if not a or not b:
        return 0.0
    match_dist = max(len(a), len(b)) // 2 - 1
    if match_dist < 0:
        match_dist = 0
    a_match = [False] * len(a)
    b_match = [False] * len(b)
    matches = 0
    for i, ca in enumerate(a):
        lo = max(0, i - match_dist)
        hi = min(i + match_dist + 1, len(b))
        for j in range(lo, hi):
            if b_match[j] or b[j] != ca:
                continue
            a_match[i] = b_match[j] = True
            matches += 1
            break
    if matches == 0:
        return 0.0
    transpositions = 0
    k = 0
    for i in range(len(a)):
        if not a_match[i]:
            continue
        while not b_match[k]:
            k += 1
        if a[i] != b[k]:
            transpositions += 1
        k += 1
    transpositions //= 2
    return (matches / len(a) + matches / len(b)
            + (matches - transpositions) / matches) / 3.0


def jaro_winkler(a: str, b: str) -> float:
    a = (a or "").strip().lower()
    b = (b or "").strip().lower()
    j = _jaro(a, b)
    prefix = 0
    for ca, cb in zip(a, b):
        if ca == cb and prefix < 4:
            prefix += 1
        else:
            break
    return j + prefix * 0.1 * (1 - j)


def _tokens(s: Optional[str]) -> set:
    if not s:
        return set()
    cleaned = "".join(c if c.isalnum() else " " for c in s.lower())
    stop = {"inc", "llc", "ltd", "co", "corp", "the", "and", "gmbh", "sa"}
    return {t for t in cleaned.split() if t and t not in stop}


def token_set_ratio(a: Optional[str], b: Optional[str]) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    inter = ta & tb
    return len(inter) / len(ta | tb)


def name_similarity(a: Optional[str], b: Optional[str]) -> float:
    """Blend whole-string Jaro-Winkler with order-independent token overlap."""
    jw = jaro_winkler(a or "", b or "")
    ts = token_set_ratio(a, b)
    return round(max(jw, (jw + ts) / 2), 4)


def company_similarity(a: Optional[str], b: Optional[str]) -> float:
    if not a or not b:
        return 0.0
    return round(max(jaro_winkler(a, b), token_set_ratio(a, b)), 4)


# --------------------------------------------------------------------------- #
# Data shapes
# --------------------------------------------------------------------------- #

@dataclass
class Person:
    """A subset of the Twenty golden-record Person, identity + engine fields."""
    id: str
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    company_name: Optional[str] = None
    last_enriched_at: Optional[str] = None
    enrichment_source: Optional[str] = None
    lifecycle_stage: Optional[str] = None
    sourced_from: Optional[str] = None
    sourced_at: Optional[str] = None
    do_not_contact: bool = False
    active_campaign_membership_id: Optional[str] = None
    manual_overrides: set = field(default_factory=set)

    def lk(self) -> Optional[str]:
        return normalize_linkedin(self.linkedin_url)

    def ek(self) -> Optional[str]:
        return normalize_email(self.email)


@dataclass
class Candidate:
    """An incoming contact from Apollo / Clay / LinkedIn."""
    source: str
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    company_name: Optional[str] = None
    last_enriched_at: Optional[str] = None
    enrichment_source: Optional[str] = None
    lifecycle_stage: Optional[str] = None
    sourced_from: Optional[str] = None

    def lk(self) -> Optional[str]:
        return normalize_linkedin(self.linkedin_url)

    def ek(self) -> Optional[str]:
        return normalize_email(self.email)


# --------------------------------------------------------------------------- #
# RL-439: identity resolver -- match keys + precedence
# --------------------------------------------------------------------------- #

# Outcomes
MATCH = "match"                 # exactly one Person via an exact key
NO_MATCH = "no-match"           # net-new; no exact key, no fuzzy candidate
FUZZY_CANDIDATE = "fuzzy-candidate"  # no exact key; >=1 name+company candidate
COLLISION = "collision"         # exact-key data-quality collision; halt to QA

SURFACE_THRESHOLD = 0.72        # >= surfaces a fuzzy candidate to the QA queue
HIGH_CONFIDENCE = 0.90          # informational only; fuzzy NEVER auto-merges


def _index(people):
    by_lk, by_ek = {}, {}
    for p in people:
        if p.lk():
            by_lk.setdefault(p.lk(), []).append(p)
        if p.ek():
            by_ek.setdefault(p.ek(), []).append(p)
    return by_lk, by_ek


def resolve(candidate: Candidate, people):
    """Resolve a candidate against the Person store.

    Precedence: exact linkedinUrl > exact email > fuzzy(name+company) > net-new.
    Returns a dict describing the outcome (never writes).
    """
    by_lk, by_ek = _index(people)
    lk, ek = candidate.lk(), candidate.ek()

    lk_hits = by_lk.get(lk, []) if lk else []
    ek_hits = by_ek.get(ek, []) if ek else []

    # exact-key collisions are a data-quality problem -> human QA, never auto.
    if len(lk_hits) > 1:
        return _result(COLLISION, candidate, matched_by="linkedinUrl",
                       persons=lk_hits,
                       reason="multiple Persons share this linkedinUrl")
    if len(ek_hits) > 1 and not lk_hits:
        return _result(COLLISION, candidate, matched_by="email",
                       persons=ek_hits,
                       reason="multiple Persons share this email")

    lk_person = lk_hits[0] if len(lk_hits) == 1 else None
    ek_person = ek_hits[0] if len(ek_hits) == 1 else None

    # both keys resolve, but to DIFFERENT persons -> cross-key merge candidate.
    if lk_person and ek_person and lk_person.id != ek_person.id:
        return _result(COLLISION, candidate, matched_by="cross-key",
                       persons=[lk_person, ek_person],
                       reason="linkedinUrl and email resolve to different "
                              "Persons; potential two-record merge")

    if lk_person:
        return _result(MATCH, candidate, matched_by="linkedinUrl",
                       persons=[lk_person],
                       fills_missing_key=_missing_key(lk_person, candidate))
    if ek_person:
        return _result(MATCH, candidate, matched_by="email",
                       persons=[ek_person],
                       fills_missing_key=_missing_key(ek_person, candidate))

    # no exact key -> try fuzzy name+company
    fuzzy = score_fuzzy_candidates(candidate, people)
    surfaced = [f for f in fuzzy if f["score"] >= SURFACE_THRESHOLD]
    if surfaced:
        return _result(FUZZY_CANDIDATE, candidate, matched_by="fuzzy",
                       persons=[], reason="no exact key; name+company match",
                       fuzzy=surfaced)
    return _result(NO_MATCH, candidate, matched_by=None, persons=[])


def _missing_key(person: Person, candidate: Candidate) -> Optional[str]:
    """Does the candidate supply a channel key the matched Person lacks?"""
    if candidate.lk() and not person.lk():
        return "linkedinUrl"
    if candidate.ek() and not person.ek():
        return "email"
    return None


def _result(outcome, candidate, matched_by, persons, reason=None,
            fills_missing_key=None, fuzzy=None):
    return {
        "outcome": outcome,
        "matched_by": matched_by,
        "person_ids": [p.id for p in persons],
        "fills_missing_key": fills_missing_key,
        "reason": reason,
        "fuzzy_candidates": fuzzy or [],
        "candidate_source": candidate.source,
        "candidate_name": candidate.name,
    }


def score_fuzzy_candidates(candidate: Candidate, people):
    """RL-441: score name+company similarity for non-exact-key candidates."""
    out = []
    for p in people:
        # only fuzzy-match records that do NOT already share an exact key
        if candidate.lk() and candidate.lk() == p.lk():
            continue
        if candidate.ek() and candidate.ek() == p.ek():
            continue
        ns = name_similarity(candidate.name, p.name)
        cs = company_similarity(candidate.company_name, p.company_name)
        domain_match = (email_domain(candidate.email) is not None
                        and email_domain(candidate.email) == email_domain(p.email))
        # company-weighted blend; a shared email domain nudges confidence up.
        score = round(0.65 * ns + 0.35 * cs + (0.05 if domain_match else 0), 4)
        score = min(score, 1.0)
        out.append({
            "person_id": p.id,
            "person_name": p.name,
            "score": score,
            "evidence": {
                "name_score": ns,
                "company_score": cs,
                "shared_email_domain": domain_match,
            },
        })
    out.sort(key=lambda r: r["score"], reverse=True)
    return out


# --------------------------------------------------------------------------- #
# RL-440: auto-merge + survivorship
# --------------------------------------------------------------------------- #

# Field classes drive survivorship behaviour.
IDENTITY_KEYS = ("linkedin_url", "email")          # fill-if-empty only
ENRICHMENT_FIELDS = ("lifecycle_stage", "enrichment_source",
                     "last_enriched_at")            # freshest-wins
SHARED_FILL_FIELDS = ("name", "company_name")      # fill-if-empty only
# sourced_from / sourced_at are set-once provenance (kept earliest, never refreshed)


def _fresher(candidate_ts, person_ts) -> bool:
    if not candidate_ts:
        return False
    if not person_ts:
        return True
    try:
        return _parse(candidate_ts) > _parse(person_ts)
    except ValueError:
        return False


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def plan_merge_from_candidate(person: Person, candidate: Candidate) -> dict:
    """RL-440: dry merge plan folding a candidate into an existing Person.

    Additive + non-destructive. Returns field-level operations; performs no
    write. Divergent populated identity values are never overwritten -- they
    are flagged as conflicts for the QA queue.
    """
    set_ops, fill_ops, conflicts, audit = {}, {}, [], []

    # identity keys: fill-if-empty only, divergence -> conflict
    for fld in IDENTITY_KEYS:
        cval = getattr(candidate, fld)
        pval = getattr(person, fld)
        if not cval:
            continue
        if not pval:
            fill_ops[fld] = cval
            audit.append(f"fill {fld} from {candidate.source}")
        elif _norm(fld, cval) != _norm(fld, pval):
            conflicts.append({"field": fld, "existing": pval,
                              "incoming": cval, "source": candidate.source})

    # shared descriptive fields: fill-if-empty only
    for fld in SHARED_FILL_FIELDS:
        cval = getattr(candidate, fld)
        if cval and not getattr(person, fld):
            fill_ops[fld] = cval
            audit.append(f"fill {fld} from {candidate.source}")

    # engine enrichment fields: freshest-wins, manual override respected
    fresher = _fresher(candidate.last_enriched_at, person.last_enriched_at)
    for fld in ENRICHMENT_FIELDS:
        cval = getattr(candidate, fld)
        if not cval:
            continue
        if fld in person.manual_overrides:
            audit.append(f"skip {fld}: manual override on record")
            continue
        pval = getattr(person, fld)
        if not pval:
            fill_ops[fld] = cval
            audit.append(f"fill {fld} from {candidate.source}")
        elif cval != pval and fresher:
            set_ops[fld] = cval
            audit.append(f"refresh {fld} (incoming enrichment is newer)")
        elif cval != pval:
            audit.append(f"keep {fld}: incoming not newer")

    return {
        "kind": "merge-candidate-into-person",
        "survivor_id": person.id,
        "fill_ops": fill_ops,
        "set_ops": set_ops,
        "conflicts": conflicts,
        "audit": audit,
        "writes": "DRY -- no Twenty writes performed",
        # every Twenty write is gated; divergent identity values route to QA
        # instead of an auto-merge.
        "requires_approval": True,
        "route": "qa-review" if conflicts else "merge-approval",
    }


def plan_merge_two_persons(a: Person, b: Person) -> dict:
    """RL-440: dry plan to fold two Person records that are the same human.

    Picks a survivor, folds the loser's missing keys/fields additively,
    re-points the active campaign membership, marks the loser merged
    (non-destructive). No deletes, no writes.
    """
    survivor, loser = _pick_survivor(a, b)
    fill_ops, conflicts, audit = {}, [], []

    for fld in IDENTITY_KEYS + SHARED_FILL_FIELDS:
        sval, lval = getattr(survivor, fld), getattr(loser, fld)
        if lval and not sval:
            fill_ops[fld] = lval
            audit.append(f"fill {fld} from loser {loser.id}")
        elif sval and lval and _norm(fld, sval) != _norm(fld, lval) and fld in IDENTITY_KEYS:
            conflicts.append({"field": fld, "survivor": sval, "loser": lval})

    membership = (survivor.active_campaign_membership_id
                  or loser.active_campaign_membership_id)
    if not survivor.active_campaign_membership_id and loser.active_campaign_membership_id:
        audit.append("re-point activeCampaignMembershipId from loser to survivor")

    return {
        "kind": "merge-two-persons",
        "survivor_id": survivor.id,
        "loser_id": loser.id,
        "fill_ops": fill_ops,
        "active_campaign_membership_id": membership,
        "loser_action": "set do_not_contact=true to suppress double-contact; "
                        "no delete, no mergedInto field exists in the schema -> "
                        "flag the pair to operator/QA for any true row dedup",
        "conflicts": conflicts,
        "audit": audit,
        "writes": "DRY -- no Twenty writes performed",
    }


def _pick_survivor(a: Person, b: Person):
    # 1. the one with an active campaign membership wins
    if bool(a.active_campaign_membership_id) != bool(b.active_campaign_membership_id):
        return (a, b) if a.active_campaign_membership_id else (b, a)
    # 2. oldest sourced record wins (stable history)
    aa, bb = a.sourced_at or "9999", b.sourced_at or "9999"
    if aa != bb:
        return (a, b) if aa < bb else (b, a)
    # 3. most complete record wins
    return (a, b) if _completeness(a) >= _completeness(b) else (b, a)


def _completeness(p: Person) -> int:
    return sum(1 for f in (p.linkedin_url, p.email, p.name, p.company_name,
                           p.lifecycle_stage, p.sourced_from) if f)


def _norm(fld: str, val: str):
    if fld == "linkedin_url":
        return normalize_linkedin(val)
    if fld == "email":
        return normalize_email(val)
    return (val or "").strip().lower()


# --------------------------------------------------------------------------- #
# RL-441: review-queue item construction
# --------------------------------------------------------------------------- #

def build_queue_item(resolution: dict) -> dict:
    """Shape a FUZZY_CANDIDATE / COLLISION resolution into a QA queue item."""
    top = resolution["fuzzy_candidates"][0] if resolution["fuzzy_candidates"] else None
    return {
        "candidate": resolution["candidate_name"],
        "source": resolution["candidate_source"],
        "reason": resolution["reason"] or resolution["outcome"],
        "matched_person_ids": resolution["person_ids"] or (
            [top["person_id"]] if top else []),
        "score": top["score"] if top else None,
        "evidence": top["evidence"] if top else None,
        "decision": "pending",          # reviewer sets: merge | reject
        "auto_merge": False,            # fuzzy NEVER auto-merges
    }
