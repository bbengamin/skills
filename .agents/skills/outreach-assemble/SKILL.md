---
name: outreach-assemble
description: Run the assemble stage of an outbound-engine run - build the omnichannel campaign segment and grounded personalization assets (LinkedIn + email) for leads that passed enrich and gate. Use when the operator wants to assemble or resume assembling a run's outreach assets, draft channel messages and personalization, or prepare a segment before push. Bulk stage with a per-lead personalization fallback; writes asset references through twenty-engine-sync; builds assets only, never sends.
---

# Outreach Assemble

Run the assemble stage for one outreach run: turn the eligible, enriched segment into omnichannel outreach assets ready for push. This is a bulk stage with a per-lead personalization fallback. Build assets only; do not create the sending-tool list and do not send. Write asset references through `twenty-engine-sync`.

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

Use the worker/subagent pattern from `run-contract.md` for large Twenty segment
reads, personalization sample QA, and per-lead personalization fallbacks when
the current client supports workers. The parent session owns the message
structure, QA decision, and Paperclip checkpoint.

1. Resume. Read the Run Record. Confirm `assemble` is in the run's stage scope and read its checkpoint.
   - If `assemble` is `done`, stop and report.
   - Read the campaign's offer or CTA, proof and source material, the channels in scope (for example LinkedIn and email), the output definition, and the QA gate.
   - Done when the channels, offer, proof, and current counts are stated.
2. Confirm the eligible segment. Assemble operates only on leads that passed enrich and gate. Read that subset of the Twenty segment; exclude suppressed, unreachable, or un-enriched leads.
3. Build the omnichannel segment. For each in-scope channel, draft the message structure grounded in the approved campaign: the offer, the CTA, and the proof or source material. Define the personalization variables drawn from enriched Twenty fields.
   - Done when each channel has a reviewed message structure and a named set of personalization variables.
4. Personalize. Fill personalization in bulk through templates and merge variables. For leads whose personalization needs bespoke judgment, run the Ralph per-unit personalization loop from `run-contract.md`: one lead at a time, grounded in that lead's enriched data.
   - Ground every claim in enriched Twenty data and approved campaign material. Do not assert anything not supported by that source.
5. Write back. Through `twenty-engine-sync`, write the assembled-asset reference and per-lead personalization to each lead's Twenty record.
6. Checkpoint. Write assemble counts (assets built, personalized, skipped, errored) and move `assemble` to `qa`.
   - Done when every eligible lead has an assembled-asset reference or an explicit skip reason, and the counts sum to the eligible total.
7. QA gate. Present the assembled assets against the run's QA gate: grounding, channel fit, and message quality. On pass, set `assemble` to `done`. On fail, set it to `revise` or `stopped` with a comment.

## Boundaries

- Builds assets, does not push or send. Creating the list in the sending tool and attaching it to a campaign is the push stage; sending is automatic in-tool.
- Grounded only. Personalization must be supported by enriched Twenty data and approved campaign proof, offer, and CTA. No ungrounded claims.
- All Twenty writes go through `twenty-engine-sync`. Never write Twenty directly.
- Eligible segment only. Do not assemble assets for suppressed, unreachable, or un-enriched leads.
- Honor caps and stop conditions, and get approval before CRM writes.
