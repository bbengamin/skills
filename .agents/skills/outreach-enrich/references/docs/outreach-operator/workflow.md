# Outreach Operator Workflow

Outreach Operator skills run the outbound engine as an operator-driven pipeline. They begin where growth planning ends: the strategy plane has already decided the campaign, ICP, wedge, offer, and success signal, and triage has marked the work ready. Outreach skills turn that into real movement on a lead list.

Two planes, two sources of truth:

- Strategy plane: Paperclip owns campaign, ICP, wedge, proof, offer, CTA, success signal, and kill/continue.
- Operations plane: Twenty owns the lead, account, and contact records and their per-lead progress.

```text
... outbound-triage -> outreach-clarify -> outreach-record-run
    -> [ source -> resolve -> enrich* -> gate -> assemble -> push/attach ]
    -> outreach-review -> (signal back to strategy)
```

The `*` on enrich marks the only stage that is a per-lead Ralph loop. Every other stage is bulk: configure the tool, trigger it, reconcile results to Twenty, then stop at a QA gate.

## Run Record And Checkpoint

A run is durable, not a chat session. Every outreach skill reads and writes one Paperclip Run Record so the operator can drop the session and resume later without losing place.

Each skill follows the same three beats:

1. Resume - read the Run Record and the Twenty segment counts before acting. Never hold run state only in chat.
2. Act - do only the current stage named in the Run Record.
3. Checkpoint - write stage status and counts back to the Run Record once the step's completion criterion is met.

Per-lead progress lives in Twenty fields, never copied into the Run Record. See `control-plane.md`.

## 1. Outreach Clarify

Use `outreach-clarify` to pin the config of one concrete run. It consumes an approved, triaged campaign and resolves stage scope, ICP filters, list scope, tools, enrichment providers, caps, suppression, QA gates, and stop conditions. Non-mutating. It produces an Outreach Run Spec.

## 2. Outreach Record Run

Use `outreach-record-run` after the operator approves the Run Spec. It writes the Run Record into Paperclip and binds it to a Twenty segment. First mutating step.

## 3. Stage Runners

Run one stage at a time against the list. Operator stage runners orchestrate; the engine skills do the per-person Twenty work.

- source - filtered sourcing into idempotent Twenty ingest.
- resolve - identity match and golden-record merge, with a per-item review loop for fuzzy matches.
- enrich* - per-lead Ralph worker over a pluggable provider waterfall, cheapest source first.
- gate - dedup, TTL, suppression, and routing over the list.
- assemble - build the omnichannel segment and personalization assets.
- push/attach - create the list in the sending tool and attach it to a campaign. Operator-gated.

Sending is automatic in the sending tool once the list is attached. v1 has no operator send step.

## Engine Skill Delegation

Stage runners do not reimplement engine work. They delegate the per-person decisions and Twenty writes to the existing engine-side company skills:

- `eligibility-gate` returns the per-person verdict (reuse / re-enrich / source / suppress / skip) and routing. Decision-only. The gate stage uses it before acting on each person.
- `twenty-engine-sync` performs the additive, dry-run-first Twenty work: query by identity, idempotent match-or-create, golden-record merge, fuzzy-match handoff to human QA, and suppression/routing writes. The source, resolve, enrich, and assemble stages route their Twenty reads and writes through it.

The operator stage runners own batch scope, caps, checkpoints, and QA gates; the engine skills own the per-person verdict and the CRM mutation.

## 4. Outreach Review

Use `outreach-review` to QA a run, make the kill/continue call, and write the signal back to Paperclip, which feeds the next strategy loop.

## Mutation Rule

Outreach skills may inspect Paperclip and Twenty freely. They must present proposed Run Records, stage actions, CRM writes, tool configuration, and list pushes before mutating, and they must respect each stage's caps and approval gates.

## Deferred

Out of scope for v1: autonomous sending, deliverability infrastructure, scheduling automation, analytics dashboards, full revenue attribution, autonomous reply handling, and the reusable enrichment agent build (gated separately).
