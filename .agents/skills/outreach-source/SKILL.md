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
3. Discover and bind the available source tools for this client. Tool namespaces vary by MCP client and connector, so do not assume a fixed prefix. Search the available tools for the required capabilities, inspect their schemas, and record the bound names before using them.
   - Required Apollo capabilities are: auth or connection status when available, API usage or credit/limit status, people search, and enrichment or match if the run requires revealed work emails. Organization/company search is optional because some Apollo surfaces charge for non-empty organization searches.
   - Accept either direct Apollo MCP tools (for example names ending in `apollo_mixed_people_api_search`, `apollo_mixed_companies_search`, or similar) or a gateway pattern such as Composio search plus multi-execute over `APOLLO_*` slugs.
   - If several surfaces exist, prefer the one with complete schemas and clear connection or credit guidance. Use the gateway path only after its discovery tool confirms an active Apollo connection and returns exact slugs and schemas.
   - Discover `twenty-engine-sync` before any CRM write. If that engine surface is not available, stop after sourcing or enrichment with a report; do not write Twenty directly and do not mark source as ingested.
   - Done when the report names the actual tools available in this client, the selected source surface, the selected Twenty engine surface if present, the required input fields, and any missing capability or permission.
4. Configure and dry-run the source query. First check auth/connection status and usage or credit limits when the bound surface supports it. Then project the result-set size, a small sample, and the credit or cost estimate against caps. Mutate nothing.
   - Direct Apollo people search is a dry sourcing action when it only returns prospect records without enriching emails or phones. Organization search, enrichment, bulk enrichment, imports, and persistent list creation can consume credits or create external state; treat them as approval-gated unless the tool schema explicitly says they are free and read-only.
   - Done when the projected list and its cost are shown and compared to the caps.
5. Ask for approval before pulling. The pull is an external-tool action and leads to CRM writes.
6. Pull within caps, then reconcile every sourced person into Twenty through `twenty-engine-sync` (idempotent match-or-create, additive). Consult `eligibility-gate` where the per-person verdict decides whether to ingest, reuse, or suppress. Record sourcing provenance on each record.
   - Also bind every ingested or reused person to a durable run segment that the next stages can query, such as the Run Record's Twenty campaign/list/membership pointer. A generic provenance field like `sourcedFrom=APOLLO` is not enough because it mixes runs.
   - When the segment is represented as a Twenty Campaign, create or reuse a `DRAFT` campaign/list object and attach people with campaign memberships named with the run label. Do not bind sending accounts, do not activate the campaign, and do not push to any sending tool.
   - Read back the segment pointer and count before checkpointing; if the segment cannot be read by run id, campaign id, run label, or another stable pointer named in the Run Record, stop with a repair plan instead of marking the source output ready.
   - Stop and checkpoint as `stopped` if a cap or stop condition trips; never exceed a cap to finish the batch.
7. Reconcile and checkpoint. Write source counts to the Run Record: sourced, ingested, matched, suppressed or deduped, and errored. Move `source` to `qa`.
   - Done when every person from the pull is accounted for in Twenty with provenance, and the counts sum to the pulled total.
8. QA gate. Present the ingested batch summary against the run's QA gate. On pass, set `source` to `done`. On fail, set it to `revise` or `stopped` with a comment.

## Tools

Apollo is the primary source, but the MCP namespace is client-dependent. Discover the actual callable names at run time and bind by capability:

- Direct Apollo tools: look for people search, people match or bulk match, usage/credit tools, profile/auth/status if present, and organization/company search when needed, even if the namespace or prefix differs. In one observed client these appeared as `Appolo_apollo_mixed_people_api_search`, `Appolo_apollo_people_bulk_match`, and `Appolo_apollo_usage_stats_credit_usage_stats`.
- Composio gateway: look for a search/discovery tool and a multi-execute tool; use the discovery response to confirm an active Apollo connection and exact `APOLLO_*` slugs such as `APOLLO_GET_AUTH_STATUS`, `APOLLO_VIEW_API_USAGE_STATS`, `APOLLO_ORGANIZATION_SEARCH`, and `APOLLO_PEOPLE_SEARCH`.
- Grinfi and file import alternatives: discover list/import capabilities by schema before use; imports create external jobs and require approval.
- Twenty ingest: route through `twenty-engine-sync`, not direct Twenty tools.

Never invent tool names or argument fields. If the selected surface only exposes partial Apollo support, report the missing capability and stop before sourcing. See `tool-map.md`.

## Boundaries

- Bulk stage, not a per-lead loop. Source fills the list and provenance; channel-key enrichment is the enrich stage.
- All Twenty writes go through `twenty-engine-sync`. Never write Twenty directly, and never send or spend send credits.
- Honor caps and suppression. Stop at the cap and checkpoint what was reached.
- Approval-gated. Get approval before the external pull and before CRM writes; the dry-run comes first.
- Stay in this run. Source only the run's segment under its filters; do not widen the ICP or start another stage.
