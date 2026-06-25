# Outreach Operator Control Plane

Outreach runs split state across two sources of truth. Keep each fact in exactly one of them.

- Paperclip owns run intent and signal: which campaign, the Run Record, stage status, caps, QA gates, kill/continue.
- Twenty owns lead data and per-lead progress: the lead, account, and contact records and the fields that say how far each one has moved through the pipeline.

Never duplicate per-lead progress into Paperclip, and never treat a chat transcript as run state.

## Run Record

The Run Record is the operations-plane analog of a Strategy Artifact: one Paperclip artifact per run that captures enough to drop and resume the run. Keep it minimal.

A Run Record holds:

- link to the approved campaign or strategy parent issue
- stage scope for this run (which of source, resolve, enrich, gate, assemble, push)
- ICP slice and the concrete sourcing filters
- the Twenty segment pointer (how to find this run's leads in Twenty)
- tools per stage, and for enrich the provider waterfall order
- caps: budget or credit caps, volume caps, rate limits
- suppression, dedup, consent, and compliance boundaries
- the channel keys or output fields that define "done enough"
- QA gates and kill/continue thresholds
- success signal and stop conditions
- a stage checklist with one status per stage

It must not hold per-lead values, enrichment results, or message bodies. Those live in Twenty.

## Checkpoint

A checkpoint is a write to the Run Record's stage checklist plus counts. Skills checkpoint only after a step's completion criterion is met, and they resume by reading the latest checkpoint. A checkpoint is both a save point to resume from and a gate the run must pass before the next stage.

Stage status values:

- `pending` - not started.
- `running` - in progress; counts show how far.
- `qa` - stage output awaiting the operator's QA gate.
- `done` - QA passed; the next stage may start.
- `stopped` - a cap, stop condition, or kill decision halted the stage.

## Per-Lead Progress In Twenty

Twenty fields, not the Run Record, carry per-lead state: sourcing provenance, identity resolution status, enrichment status with provider, confidence, and cost, eligibility decision, assembled-asset reference, and outcome or reply signal. The enrich Ralph loop reads "the next lead whose enrichment status is unset" from Twenty, which makes the loop resumable and crash-safe.

## Stage Ownership

Operator stage runners own batch scope, caps, checkpoints, and QA gates. The per-person verdict and the Twenty mutation belong to the engine skills.

- source: filters to a list; idempotent ingest to Twenty via `twenty-engine-sync`.
- resolve: identity match, precedence, and golden-record merge via `twenty-engine-sync`; fuzzy matches go to its human-QA review loop.
- enrich: per-lead waterfall, cheapest source first, stop when required keys are filled; write values, provider, confidence, and cost back to Twenty via `twenty-engine-sync`.
- gate: per-person verdict from `eligibility-gate` (reuse / re-enrich / source / suppress / skip); dedup, TTL, suppression, and routing writes via `twenty-engine-sync`.
- assemble: omnichannel segment and personalization assets; any Twenty write via `twenty-engine-sync`.
- push: create the list in the sending tool and attach to a campaign; sending is automatic in-tool.

## Mutation Rule

Outreach skills inspect freely. They present proposed Run Records, CRM writes, tool configuration, and list pushes before mutating, and they honor each run's caps, suppression rules, and approval gates. CRM writes go through `twenty-engine-sync` (additive, dry-run first); no sending and no credit spend in v1.
