# Twenty filter strategy (push suppression into the query)

Reliability at batch scale comes from letting the database do the obvious
elimination, so the gate (and the agent) never reason per-lead about state a
filter can express. Fetch only plausibly-eligible candidates; let the gate
decide the rest.

## Filter at fetch

Use `find_many_people` with an explicit `select` and these filters combined with
`and`, so suppressed and parked people never enter the batch:

- exclude hard suppression: `doNotContact = false` AND `lifecycleStage != CUSTOMER`.
- exclude active-elsewhere: `activeCampaignMembershipId IS NULL` (a person with no
  active membership cannot be active in another campaign). People whose active
  membership is the target campaign are fetched separately when re-running an
  enrolled set.
- scope to the candidate set (ICP filter, sourcedFrom, etc.) for the campaign.

The blocklist substrate (`blocklists`) is referenced, not recreated; intersect
candidate identity keys against it in the same pass.

## What stays in the gate

The query cannot cheaply express the rest, so the deterministic gate still owns:

- TTL cooldown: needs the most recent `campaignTouch.touchedAt` per person vs
  `now - ttlDays`. Either join touches in the fetch or resolve per person, then
  let the gate compare.
- the `source` / `re-enrich` / `reuse` split: depends on `lastEnrichedAt`
  freshness and required-channel-key presence.
- connection-aware routing.

## Why split it this way

Filters are deterministic, cheap, and auditable, and they shrink the batch the
gate processes. The gate then runs as code over a small, pre-cleaned set, which
keeps the per-person decision fast, consistent, and re-runnable — and keeps the
LLM agent out of the rules-engine role it is unreliable at.
