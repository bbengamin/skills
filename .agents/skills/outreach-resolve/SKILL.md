---
name: outreach-resolve
description: Run the resolve stage of an outbound-engine run - identity match and golden-record merge over the sourced segment, delegating the per-person decision to twenty-engine-sync. Use when the operator wants to resolve or resume resolving a run's leads, dedupe sourced contacts into golden records, or route fuzzy matches to human QA before enrich. Bulk stage; the per-person verdict and Twenty writes belong to twenty-engine-sync; stops at a QA gate.
---

# Outreach Resolve

Run the resolve stage for one outreach run: turn the sourced segment into clean golden records. This is a bulk stage. The per-person identity decision, merge, and write belong to `twenty-engine-sync`; this skill owns batch scope, caps, checkpoints, and the QA gate.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/outreach-operator/run-contract.md`
- `references/docs/outreach-operator/control-plane.md`

Open when checkpointing to Paperclip or choosing a surface:

- `references/docs/outreach-operator/workflow.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

## Process

Follow the bulk-stage pattern in `run-contract.md`. The per-person work is `twenty-engine-sync`.

1. Resume. Read the Run Record. Confirm `resolve` is in the run's stage scope and read its checkpoint. Confirm `source` is `done`.
   - Done when you can state whether this is a fresh resolve or a resume, and the current counts.
2. Read the sourced segment from Twenty: the run's leads that have been ingested but not yet resolved.
3. Resolve through `twenty-engine-sync`. For each contact, run identity match, precedence, and golden-record merge. Send ambiguous pairs to its fuzzy-match human-QA queue rather than auto-merging.
   - Auto-merge only the matches `twenty-engine-sync` returns as confident; never auto-merge a fuzzy match.
   - Stop and checkpoint as `stopped` if a cap or stop condition trips.
4. Human-QA review. For fuzzy matches, run the per-item review loop from `run-contract.md`: one ambiguous pair at a time, with the operator's merge-or-split decision. This is operator-gated; do not merge a fuzzy pair without approval.
5. Checkpoint. Write resolve counts (merged, created, queued for QA, errored) and move `resolve` to `qa`.
   - Done when every sourced lead is a golden record, queued for QA, or carries an explicit skip reason, and the counts sum to the sourced total.
6. QA gate. Present the resolved batch and the fuzzy-QA outcomes against the run's QA gate. On pass, set `resolve` to `done`. On fail, set it to `revise` or `stopped` with a comment.

## Boundaries

- Bulk stage. Resolve dedupes and merges; it does not enrich or send.
- The verdict belongs to `twenty-engine-sync`. Do not reimplement identity rules or write Twenty directly.
- Never auto-merge fuzzy matches. Route them to human QA; merges there are operator-gated.
- Honor caps and stop conditions, and stay within the run's segment.
