---
name: outreach-clarify
description: Run a non-mutating clarification session that pins the config of one concrete outreach run before it touches lead data. Use when the operator wants to run a stage of the outbound engine (source, resolve, enrich, gate, assemble, push) on a real lead list, kick off or resume a Run Record, or turn an approved campaign into an executable run. Reads Paperclip and Twenty freely; mutates nothing.
---

# Outreach Clarify

Turn an approved, triaged campaign into a precise Outreach Run Spec for one run. Do not mutate Paperclip or Twenty.

This skill is the front of the operations plane. The strategy plane already decided campaign, ICP, wedge, offer, and success signal; outreach-clarify decides how to run one stage on one lead list, with explicit caps and gates.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/outreach-operator/workflow.md`
- `references/docs/outreach-operator/control-plane.md`

Open when the run consumes upstream strategy or needs lifecycle rules:

- `references/docs/growth-operator/control-plane.md`
- `references/docs/paperclip-operator/control-plane.md`

## Process

1. Resume before clarifying. Look for an existing Run Record for this campaign and stage scope.
   - If one exists, read its latest checkpoint and the Twenty segment counts, then clarify only the gaps and any config the operator wants to change.
   - If none exists, clarify a fresh run.
   - Done when you can state, in one line, whether this is a new run or a resume and what is already settled.
2. Confirm the upstream campaign is approved and triaged. If the work is still strategy or planning, stop and route to the growth or outbound skills instead of clarifying a run.
3. Grill one question at a time. Walk the run-config tree below, resolving dependencies before dependents: campaign before stage scope, stage scope before tools, filters before list scope, output definition before QA gates, caps before send-adjacent stages. For each question, give your recommended answer so the operator can accept, edit, or reject quickly. Never bundle questions.
   - If an answer is discoverable from Paperclip, Twenty, the Run Record, or the repo, inspect it instead of asking.
   - If the campaign references a Paperclip wiki page or captured source as ICP or proof, use `paperclip-wiki-fetch` before asking what that material can answer.
4. Maintain a decision ledger: Established, Assumptions, Open branches, Contradictions. Use it to choose the next highest-leverage question. A run whose ICP slice, list scope, output definition, caps, and stop conditions are still vague is not ready to record.
5. Produce the Outreach Run Spec when every required field below is resolved, has a known source to inspect, or is an explicit open question.
   - Done when the spec is complete enough that `outreach-record-run` could write a Run Record without re-interviewing the operator.
6. Hand off. State that the next step is `outreach-record-run`, and do not mutate anything yourself.

## Run-Config Fields

Resolve each. These map one-to-one onto the Run Record in `control-plane.md`.

- campaign: the approved campaign or strategy parent issue this run serves.
- stage scope: which engine stages this run covers (source, resolve, enrich, gate, assemble, push). One run may cover one stage or a contiguous span.
- ICP slice and filters: the concrete sourcing filters that define who enters the list.
- list scope: batch size and how the run's leads are identified as a Twenty segment.
- tools per stage: the tool used at each in-scope stage.
- enrichment waterfall: for an enrich-stage run, the ordered provider list, cheapest source first, and the rule for when to stop trying providers.
- output definition: the channel keys or fields that mean a lead is "done enough" for this run.
- caps: budget or credit caps, volume caps, and rate limits.
- suppression and compliance: dedup, TTL, suppression lists, consent, and account-action boundaries.
- QA gates: what the operator reviews between stages, and the kill/continue thresholds.
- success signal and stop conditions: what tells this run it worked, and what halts it.

## Boundaries

- Non-mutating: inspect Paperclip and Twenty, but create and change nothing. The first mutation belongs to `outreach-record-run`.
- Stay in the operations plane: do not re-clarify strategy, decompose issues, or plan campaigns. Route strategy work to `growth-clarify`; planning to `outbound-plan-work`; readiness to `outbound-triage`.
- v1 has no operator send step. A push-stage run ends at "list created and attached to a campaign"; sending is automatic in the sending tool. Do not clarify a send run.
- Stop and ask when stage scope crosses into sending, when caps or suppression for a send-adjacent stage are missing, when the ICP slice is unmeasurable, or when the run targets a different ICP or CTA than the approved campaign.
