# Golden-record schema (outbound engine)

Reconstructed from the RL-426 data-model spec and the `twenty-admin` Core Model.
This is the schema the identity resolver, merge, and QA queue resolve against.
Source of truth is Twenty CRM; the engine writes additively, never destructively.

## Person (identity anchor)

| Field | Role |
| --- | --- |
| `linkedinLink.primaryLinkUrl` | Identity key 1 (highest precedence) |
| `emails.primaryEmail` | Identity key 2 |
| `name` | Display / fuzzy-match input |
| `companyId` | FK to company; company name used for fuzzy match |
| `lastEnrichedAt` | Freshness signal for survivorship |
| `enrichmentSource` | Provenance (apollo, clay, linkedin, manual) |
| `linkedinConnectionState` | Connection status (lives on membership for per-campaign) |
| `sourcedFrom` / `sourcedAt` | Origin + first-seen timestamp |
| `doNotContact` | Hard suppression flag |
| `lifecycleStage` | LEAD / CONTACTED / ENGAGED / QUALIFIED / CUSTOMER / DISQUALIFIED |
| `activeCampaignMembershipId` | One-active-campaign-per-person pointer |
| `campaignMemberships[]` | Collection of memberships |

Two Person records are the **same person** if either identity key matches.

Note (as-built `96cee083`): the Person object has **no** `icpHypothesis` field. ICP hypothesis lives on `campaign.hypothesis`; per-person fit rationale lives on `campaignMembership.icpFit`.

## Campaign / CampaignMembership / campaignTouch

- `Campaign`: `channels[]` (linkedin, email), `status`, `hypothesis`.
- `CampaignMembership` (Person <-> Campaign): per-channel `sendingAccount`,
  `status` (ACTIVE = suppression authority), outcome, connection state.
- `campaignTouch`: append-only per-event touch history (`touchType`, not `type`).

## SendingAccount / EngineConfig

- `SendingAccount`: account identity per channel, `status`, `dailyLimit`.
- `EngineConfig`: `ttlDays` (default 90), suppression rule, routing rules;
  company default with per-campaign override.

## Identity precedence (used everywhere)

1. `linkedinLink.primaryLinkUrl`
2. `emails.primaryEmail`

Email and LinkedIn fields are **not** unique-constrained in Twenty, so the
engine resolves by `find_many_*` + classification rather than `upsert_*`.
