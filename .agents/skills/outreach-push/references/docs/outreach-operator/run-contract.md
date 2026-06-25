# Outreach Run Contract

The shared execution contract for outreach stage runners. Every stage runner reads it so the pipeline behaves the same way each run. It defines the two stage patterns, the gates they pass, and how they delegate to the engine skills.

## Resume, Act, Checkpoint

Every stage runner runs the same three beats from `workflow.md`:

1. Resume - read the Run Record and Twenty segment counts first. If the stage is already `done`, stop. If `running`, continue from its counts. Never hold run state only in chat.
2. Act - do only this stage, on this run's segment, within this run's caps.
3. Checkpoint - after the completion criterion is met, write stage status and counts to the Run Record.

Counts are the unit of progress: how many of the segment have been handled, deduped or suppressed, errored, and remain. A stage is resumable because its counts and per-lead state live in Twenty, not in the transcript.

## Two Stage Patterns

A stage is one of two kinds. The Run Record's stage scope says which stages run; this contract says how each kind behaves.

### Bulk Stage

For stages a tool handles in bulk (source, gate, assemble, push). The unit is the list.

1. Configure the tool from the Run Record (filters, fields, caps).
2. Dry-run: project the result set, a sample, and the cost or credit estimate against caps. Mutate nothing.
3. Approval gate before any external-tool action, CRM write, or credit spend.
4. Trigger the bulk operation within caps.
5. Reconcile every item back to Twenty through `twenty-engine-sync`, recording provenance.
6. Checkpoint counts, then move the stage to `qa` for the operator's review.

### Ralph Per-Unit Stage

For per-item judgment work with no bulk tool to trust (enrich, fuzzy-match review). The unit is one lead.

1. Read one unhandled lead from Twenty (the segment member whose stage field is unset).
2. Do exactly that one lead's work.
3. Write the result back to Twenty through `twenty-engine-sync`; record provider, confidence, and cost where the stage produces them.
4. Checkpoint counts; emit a completion sigil.
5. The driver re-invokes for the next lead until the segment is drained or a cap or stop condition trips.

Per-unit isolation keeps each iteration's context small and the loop crash-safe: a dropped run resumes by re-reading "the next unhandled lead".

## Caps And Stop Conditions

Every stage honors the Run Record's caps (budget or credit cap, volume cap, rate limit) and stop conditions. When a cap or stop condition trips, set the stage to `stopped`, checkpoint the counts reached, and report why. Never exceed a cap to finish a batch.

## Engine Skill Delegation

Stage runners orchestrate; they do not reimplement the engine.

- `eligibility-gate` returns the per-person verdict (reuse / re-enrich / source / suppress / skip) and routing. Consult it before acting on a person where the verdict affects whether to source, enrich, or suppress them.
- `twenty-engine-sync` performs all Twenty reads and writes: query by identity, idempotent match-or-create, golden-record merge, fuzzy-match handoff to human QA, and suppression or routing writes. It is additive and dry-run-first, with no sending and no credit spend.

Stage runners never write Twenty directly and never send. The operator owns batch scope, caps, checkpoints, and QA gates.

## QA Gate

A bulk stage ends at `qa`, not `done`. The operator reviews the stage's reconciled output against the Run Record's QA gate and kill/continue thresholds. On pass, the stage moves to `done` and the next stage may start. On fail, the stage moves to `revise` or `stopped` with a comment.
