"""Synthetic batch for the RL-428 eligibility-gate dry demo.

Entirely fabricated. No real people, no Twenty data. Each entry is built to land
on one canonical verdict so run_demo can assert the full distribution.
"""

from eligibility_gate import (
    Person, EngineConfig, GateInput,
    MATCH, NO_MATCH, FUZZY_CANDIDATE, COLLISION,
)

NOW = "2026-06-25T00:00:00Z"
CAMPAIGN = "camp-A"


def sample_config():
    # email-keyed person with a blocklisted email demonstrates the blocklist rule
    return EngineConfig(ttl_days=90,
                        campaign_channels=("LINKEDIN", "EMAIL"),
                        active_accounts={"LINKEDIN": "li-acct-1", "EMAIL": "em-acct-1"},
                        blocklist_keys=frozenset({"blocked@dupe-co.com"}))


def sample_inputs():
    return [
        # --- suppress ---
        GateInput(MATCH, CAMPAIGN, now=NOW, person=Person(
            id="p-active", linkedin_url="https://linkedin.com/in/a", email="a@x.com",
            name="Active Elsewhere", active_campaign_id="camp-B")),
        GateInput(MATCH, CAMPAIGN, now=NOW, person=Person(
            id="p-dnc", linkedin_url="https://linkedin.com/in/b", email="b@x.com",
            name="Do Not Contact", do_not_contact=True)),
        GateInput(MATCH, CAMPAIGN, now=NOW, person=Person(
            id="p-cust", linkedin_url="https://linkedin.com/in/c", email="c@x.com",
            name="Existing Client", lifecycle_stage="customer")),

        # --- skip ---
        GateInput(MATCH, CAMPAIGN, now=NOW, person=Person(
            id="p-cool", linkedin_url="https://linkedin.com/in/d", email="d@x.com",
            name="In Cooldown", latest_touch_at="2026-06-01T00:00:00Z",
            last_enriched_at="2026-06-01T00:00:00Z", connection_state="CONNECTED")),
        GateInput(FUZZY_CANDIDATE, CAMPAIGN, now=NOW),
        GateInput(COLLISION, CAMPAIGN, now=NOW),
        GateInput(MATCH, CAMPAIGN, now=NOW, person=Person(
            id="p-noch", linkedin_url="https://linkedin.com/in/e", email=None,
            name="No Open Channel", connection_state="DECLINED",
            last_enriched_at="2026-06-01T00:00:00Z")),

        # --- source / re-enrich / reuse ---
        GateInput(NO_MATCH, CAMPAIGN, now=NOW),
        GateInput(MATCH, CAMPAIGN, now=NOW, person=Person(
            id="p-stale", linkedin_url="https://linkedin.com/in/f", email="f@x.com",
            name="Stale Enrichment", last_enriched_at="2025-01-01T00:00:00Z",
            connection_state="CONNECTED")),
        GateInput(MATCH, CAMPAIGN, now=NOW, person=Person(
            id="p-fresh", linkedin_url="https://linkedin.com/in/g", email="g@x.com",
            name="Fresh Enrichment", last_enriched_at="2026-06-10T00:00:00Z",
            connection_state="CONNECTED")),
    ]
