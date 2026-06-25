# Decision order (ordered, with routing)

The gate evaluates these in order and returns on the first decisive step. The
order is deliberate: hard exclusions come before the `re-enrich` verdict so the
gate never recommends a Clay credit spend on a person it would suppress. (This
is a reorder of RL-428's original list, where enrichment-freshness sat at step
2; suppression now precedes it.)

Inputs per person: the RL-439 identity outcome, the matched golden record (if
any), the target campaign id + channels, the resolved `engineConfig`, and the
clock value `now`. Fields are read from the as-built golden-record schema (see
`twenty-engine-sync/references/golden-record-schema.md`).

## 1. Identity / dedup

Consume the resolver outcome (twenty-engine-sync owns resolution):

- `collision` or `fuzzy-candidate` -> `skip` (reason `awaiting-qa`). Never decide
  eligibility on an ambiguous identity; the row goes to human QA.
- `no-match` -> net-new; no suppression state to check, carry forward.
- `match` -> load the golden record, continue.

## 2. Hard suppression (matched records only)

`suppress` when any holds:

- `doNotContact = true` (reason `do-not-contact`).
- `lifecycleStage = CUSTOMER` — existing client (reason `existing-client`).
- an identity key is in the `engineConfig` blocklist substrate (reason
  `blocklist`).

Net-new people have no record, so they pass this step.

## 3. Active-campaign suppression (matched records only)

One active campaign per person, global. `suppress` (reason `active-elsewhere`)
when `activeCampaignMembershipId` points at an `ACTIVE` membership for a campaign
other than the target. If the active membership is the target campaign, this is a
re-run for an already-enrolled person — continue (the data verdict still applies).

## 4. TTL / re-contact cooldown (matched records only)

Find the most recent `campaignTouch.touchedAt`. `skip` (reason
`within-cooldown:<ttlDays>d`) when `now - touchedAt < ttlDays`. Net-new people
have no touches and pass.

## 5. Data verdict (eligible people)

- net-new (`no-match`) -> `source`.
- matched and (`lastEnrichedAt` is null OR `now - lastEnrichedAt >= ttlDays` OR a
  channel key required by the campaign's channels is missing) -> `re-enrich`.
- matched, enrichment fresh, required channel keys present -> `reuse`.

## 6. Connection-aware routing

For an actionable verdict, choose channel + a candidate sending account from
`engineConfig.routingRules` and the membership `linkedinConnectionState`:

- `CONNECTED` -> LinkedIn `message`.
- `NONE` / `PENDING` -> LinkedIn `connection_request`, else `EMAIL` if the
  campaign allows and an email key exists.
- `DECLINED` / `WITHDRAWN` -> do not re-attempt LinkedIn; route to `EMAIL` if
  eligible, else no open channel -> downgrade the verdict to `skip` (reason
  `no-open-channel`).

Pick a `sendingAccount` whose `status = ACTIVE` for the chosen channel and within
`dailyLimit`. Routing is a hint; the caller binds and stamps the account on write.
