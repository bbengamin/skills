# RL-440 — Auto-merge + survivorship rules

On an exact-key `match` (including when a new source supplies the MISSING
channel key) or when two Person records resolve to the same human, fold into one
golden record. Additive and non-destructive; every write is operator-gated.
Field names below are the as-built Twenty schema (workspace `96cee083`).

## Field classes drive survivorship

Precedence within a field: **manual override > freshest enrichment >
fill-if-empty > keep existing**.

| Class | Fields | Rule |
| --- | --- | --- |
| Identity keys | `linkedinLink`, `emails` | fill-if-empty only; a divergent populated primary is never overwritten → QA |
| Shared descriptive | `name`, `companyId`, `jobTitle`, `phones` | fill-if-empty only |
| Engine enrichment | `lifecycleStage`, `enrichmentSource`, `lastEnrichedAt` | freshest-wins by `lastEnrichedAt`; manual override wins |
| Provenance (set-once) | `sourcedFrom`, `sourcedAt` | keep earliest; never overwrite |
| Per-membership (not on Person) | `icpFit`, `linkedinConnectionState`, `outcome` | live on `campaignMembership`; union memberships, never write onto the Person row |
| History / multi-value | `campaignMemberships`, `campaignTouch`, `additionalEmails`, `secondaryLinks` | union / append, never shrink |

Note: `icpFit` is a per-person-per-campaign rationale on `campaignMembership`,
not a Person golden-record field. `hypothesis` lives on `campaign`. There is no
`icpHypothesis` field on the as-built Person object.

## Two-record merge (same human, split channels)

Twenty has no native record-merge action and no `mergedInto` field in the
as-built schema, so the engine does an **additive consolidation only**:

1. **Survivor selection**: record with an active campaign membership wins; else
   earliest `sourcedAt`; else most complete.
2. Fold the loser's missing identity keys and empty shared/enrichment fields onto
   the survivor by the field-class rules above.
3. Union the loser's `campaignMemberships`/touches onto the survivor; re-point
   `activeCampaignMembershipId` to the survivor.
4. Set the loser `doNotContact = true` to prevent double-contact.
   **No delete, no invented field, no nonexistent enum.**
5. Flag the pair to operator/QA: a true row-level dedup is structural and outside
   the engine's additive scope (needs operator action, or a `mergedIntoId` field
   added first via `twenty-admin` schema work).

## Conflict handling

Divergent populated identity values are never auto-overwritten; the merge plan
records the conflict and routes to QA. Clean merges still require approval.

## Acceptance demonstrated (dry, on the synthetic sample)

`run_demo.py` emits dry plans with zero writes: a candidate→`p-001` merge
(fills `email`, refreshes `enrichmentSource`/`lastEnrichedAt`), and a
`p-010`+`p-011` two-record consolidation (survivor keeps the active membership,
fills `email` from the loser, loser suppressed via `doNotContact`).

## Boundary

Additive / non-destructive. No Twenty writes until approved. No sending, no
credit spend.
