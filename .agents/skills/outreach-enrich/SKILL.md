---
name: outreach-enrich
description: Run the enrich stage of an outbound-engine run as a per-lead Ralph worker - enrich one lead per invocation through a cheapest-first provider waterfall, stopping as soon as the run's required channel keys are filled. Use when the operator wants to enrich or resume enriching a run's leads, fill channel keys before campaign assembly, or run the per-lead enrichment loop. Writes back through twenty-engine-sync; honors per-lead and run-level cost caps.
---

# Outreach Enrich

Run the enrich stage for one outreach run, one lead at a time. This is a Ralph per-unit stage: each invocation enriches exactly one lead, then checkpoints and emits a completion sigil so a driver can re-invoke for the next. The unit is one lead because the reasoning is per-lead; cost control comes from stopping the moment the required keys are filled.

Write back through `twenty-engine-sync`. Never write Twenty directly and never send.

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

Follow the Ralph per-unit pattern in `run-contract.md`. One lead per invocation.

1. Resume. Read the Run Record. Confirm `enrich` is in the run's stage scope and read its checkpoint counts.
   - If `enrich` is `done`, stop and report.
   - Read the run's output definition (the required channel keys), the enrichment waterfall (provider order), and the caps (per-lead cost cap and run-level credit or budget cap).
   - Done when the required keys, provider order, and caps are known and the current counts are stated.
2. Select one lead. From the Twenty segment, read the next lead whose enrichment status is unset or marked re-enrich.
   - If none remain, move `enrich` to `qa`, checkpoint, and emit a sigil marking the stage drained. Stop.
3. Gate check. Consult `eligibility-gate` for this lead's verdict. If reuse, skip, or suppress, record that outcome through `twenty-engine-sync`, checkpoint, emit a `skipped` sigil, and stop. If re-enrich or source, proceed.
4. Run the waterfall. Try providers in the configured order, cheapest first. After each provider, check whether the required keys are filled. Stop as soon as the required keys are filled, the providers are exhausted, or the per-lead cost cap is reached. Track which provider filled each key, the confidence, and the cost.
5. Write back. Through `twenty-engine-sync`, write the filled keys with provenance, provider, confidence, and cost, and set the lead's enrichment status to `enriched` or `unreachable`.
6. Checkpoint and sigil. Update the `enrich` counts (enriched, unreachable, skipped, spend). If a run-level cap tripped, set `enrich` to `stopped`. Emit the completion sigil.
   - Done when exactly one lead reached a terminal enrichment status with provenance, confidence, and cost written, counts updated, and the sigil emitted.
7. Loop. A driver re-invokes for the next lead until the segment is drained or a run-level cap or stop condition trips. When drained, `enrich` sits at `qa` for the operator's review and kill/continue call.

## Provider Waterfall

The waterfall is the durable building block, and the seed of the reusable enrichment agent (RL-417). Keep every source behind one adapter contract so providers stay swappable.

Adapter contract - each provider takes one lead and returns:

- the channel keys it could fill
- provenance for each value
- a confidence score
- the cost or credits spent

Ordering and stop rule:

- Order is cheapest first, taken from the Run Record's enrichment waterfall, not hardcoded. A typical order is existing Twenty data (free), then the metamcp providers `grinfi__enrich_leads` / `grinfi__enrich_companies`, `instantly__enrichment_enrich`, `instantly__verify_email`, then Apollo enrichment via composio (`APOLLO_PEOPLE_ENRICHMENT`), and Clay through its direct agent connection as the paid fallback. See `tool-map.md`.
- Stop the waterfall as soon as the required keys are filled. Do not call a more expensive provider once the run's output definition is satisfied.
- A per-lead cost cap bounds spend even when keys are still missing; if it trips first, mark the lead `unreachable` for this run.

## Completion Sigil

End each invocation with one sigil line so a driver can advance:

```text
RALPH: stage=enrich unit=<lead-id> status=<ok|unreachable|skipped|drained|stopped> spend=<cost> remaining=<n>
```

`ok` means the lead reached its required keys; `unreachable` means the waterfall or per-lead cap was exhausted first; `skipped` is a gate reuse/skip/suppress; `drained` means no lead was left; `stopped` means a run-level cap or stop condition halted the stage. A driver re-invokes this skill until `remaining=0` or a stop token. The driver ships with this skill at `scripts/ralph-run.sh`; run `bash scripts/ralph-run.sh --run <RUN_ID> --skill outreach-enrich --budget <cap> --agent "<agent cmd>"`.

## Boundaries

- Per-lead Ralph worker. One lead per invocation; do not batch-enrich in a single pass.
- All Twenty writes go through `twenty-engine-sync`. Never write Twenty directly and never send or spend send credits.
- Cost first. Stop the waterfall the moment the required keys are filled, and never exceed the per-lead or run-level cap; checkpoint what was reached.
- Providers stay behind the adapter contract. Read the provider order from the Run Record; do not hardcode a provider into the loop.
- Thin v1. Keep to the configured cheap providers with Clay optional; do not build the full reusable enrichment agent here. That is gated (RL-417).
