---
name: outreach-source
description: Run the source stage of an outbound-engine run - filtered sourcing (Apollo) into idempotent Twenty ingest, within the Run Record's caps. Use when the operator wants to source or resume sourcing a run's lead list, pull leads matching the ICP filters, or fill a Twenty segment before resolve and enrich. Bulk stage; reconciles every lead through twenty-engine-sync and stops at a QA gate.
---

# Outreach Source

Run the source stage for one outreach run: turn the run's ICP filters into a sourced list and ingest it idempotently into Twenty. This is a bulk stage. Reconcile every lead through `twenty-engine-sync`; do not write Twenty directly and do not enrich or send.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/outreach-operator/run-contract.md`
- `references/docs/outreach-operator/tool-map.md`
- `references/docs/outreach-operator/control-plane.md`

Open when checkpointing to Paperclip or choosing a surface:

- `references/docs/outreach-operator/workflow.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

## Process

Follow the bulk-stage pattern in `run-contract.md`.

1. Resume. Read the Run Record. Confirm `source` is in the run's stage scope and read its checkpoint.
   - If `source` is `done`, stop and report; do not re-source.
   - If `running`, read its counts and the Twenty segment, and continue from there.
   - Done when you can state whether this is a fresh source run or a resume, and the current counts.
2. Read source config from the Run Record: ICP slice and filters, source tool, volume and credit caps, and suppression rules.
3. Configure and dry-run the source query. Project the result-set size, a small sample, and the credit or cost estimate against caps. Mutate nothing.
   - Done when the projected list and its cost are shown and compared to the caps.
4. Ask for approval before pulling. The pull is an external-tool action and leads to CRM writes.
5. Pull within caps, then reconcile every sourced person into Twenty through `twenty-engine-sync` (idempotent match-or-create, additive). Consult `eligibility-gate` where the per-person verdict decides whether to ingest, reuse, or suppress. Record sourcing provenance on each record.
   - Stop and checkpoint as `stopped` if a cap or stop condition trips; never exceed a cap to finish the batch.
6. Reconcile and checkpoint. Write source counts to the Run Record: sourced, ingested, matched, suppressed or deduped, and errored. Move `source` to `qa`.
   - Done when every person from the pull is accounted for in Twenty with provenance, and the counts sum to the pulled total.
7. QA gate. Present the ingested batch summary against the run's QA gate. On pass, set `source` to `done`. On fail, set it to `revise` or `stopped` with a comment.

## Tools

Apollo is the primary source, reached through composio: `composio__COMPOSIO_SEARCH_TOOLS` with `toolkits:["APOLLO"]`, then `composio__COMPOSIO_MULTI_EXECUTE_TOOL` over `APOLLO_PEOPLE_SEARCH` / `APOLLO_ORGANIZATION_SEARCH`. Confirm the connection with `APOLLO_GET_AUTH_STATUS` before pulling. A provided CSV imports via `grinfi__import_leads_from_file`. Ingest to Twenty through `twenty-engine-sync`. See `tool-map.md`.

## Boundaries

- Bulk stage, not a per-lead loop. Source fills the list and provenance; channel-key enrichment is the enrich stage.
- All Twenty writes go through `twenty-engine-sync`. Never write Twenty directly, and never send or spend send credits.
- Honor caps and suppression. Stop at the cap and checkpoint what was reached.
- Approval-gated. Get approval before the external pull and before CRM writes; the dry-run comes first.
- Stay in this run. Source only the run's segment under its filters; do not widen the ICP or start another stage.
