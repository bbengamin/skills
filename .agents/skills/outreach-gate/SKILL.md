---
name: outreach-gate
description: Run the gate stage of an outbound-engine run - apply the per-person eligibility verdict (reuse / re-enrich / source / suppress / skip) and dedup, TTL, suppression, and routing over the run's segment. Use when the operator wants to gate or resume gating a run's leads, suppress ineligible or do-not-contact people, or route eligible leads before assembly. Bulk stage; the verdict comes from eligibility-gate and writes go through twenty-engine-sync; stops at a QA gate.
---

# Outreach Gate

Run the gate stage for one outreach run: decide who is eligible to keep moving and route or suppress the rest. This is a bulk stage. The per-person verdict belongs to `eligibility-gate` and every write belongs to `twenty-engine-sync`; this skill owns batch scope, caps, checkpoints, and the QA gate.

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

Follow the bulk-stage pattern in `run-contract.md`. The verdict is `eligibility-gate`; the writes are `twenty-engine-sync`.

Use the worker/subagent pattern from `run-contract.md` for large Twenty segment
reads, eligibility batches, suppression audits, and routing write readbacks when
the current client supports workers. The parent session owns approvals, QA
decisions, and Paperclip checkpoints.

1. Resume. Read the Run Record. Confirm `gate` is in the run's stage scope and read its checkpoint. Read the suppression, dedup, TTL, consent, and routing rules.
   - Done when the rules are known and the current counts are stated.
2. Read the segment from Twenty: the run's resolved leads not yet gated.
3. Get the verdict. For each person, get the `eligibility-gate` verdict (reuse / re-enrich / source / suppress / skip) and routing. The gate is decision-only; it does not write.
4. Apply the verdict through `twenty-engine-sync`: dedup, TTL checks, suppression, and routing. Suppress through the wired blocklists where applicable (`grinfi__add_to_leads_blacklist`, `instantly__blocklist_create`); see `tool-map.md`.
   - Never contact or queue a `suppress` or no-consent person.
   - Stop and checkpoint as `stopped` if a cap or stop condition trips.
5. Checkpoint. Write gate counts (eligible, suppressed, re-enrich, skipped, errored) and move `gate` to `qa`.
   - Done when every resolved lead carries a verdict and routing, and the counts sum to the resolved total.
6. QA gate. Present the gated batch and the suppression outcomes against the run's QA gate. On pass, set `gate` to `done`. On fail, set it to `revise` or `stopped` with a comment.

## Boundaries

- Bulk stage. Gate decides eligibility and routing; it does not enrich, assemble, or send.
- The verdict belongs to `eligibility-gate`; the writes belong to `twenty-engine-sync`. Do not reimplement the verdict or write Twenty directly.
- Suppression is hard. Never move a suppressed or no-consent person forward, and honor TTL and dedup before spend.
- Honor caps and stop conditions, and stay within the run's segment.
