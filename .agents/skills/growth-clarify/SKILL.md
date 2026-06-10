---
name: growth-clarify
description: Run a non-mutating Growth Operator clarification session for acquisition strategy that may span inbound and outbound. Use when planning repeatable acquisition, aligning creator/inbound and outbound strategy, defining growth company/team goals, or choosing durable channel/motion projects before creating Paperclip records.
---

# Growth Clarify

Turn rough acquisition intent into a structured Growth Clarification Summary. Do not mutate Paperclip.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/growth-operator/workflow.md`
- `../../../docs/growth-operator/control-plane.md`

Open Paperclip references only when lifecycle or mutation rules are needed:

- `../../../docs/paperclip-operator/control-plane.md`
- `../../../docs/paperclip-operator/workflow.md`

## Process

Ask one question at a time. For each question, provide your recommended answer.

If the answer can be discovered from the repo or Paperclip state, inspect that instead of asking.

If the operator provides a Paperclip wiki URL, wiki page path, or captured wiki source as proof or source material, use `paperclip-wiki-fetch` to read it before asking questions that the wiki material can answer. If wiki access details are missing, ask for the minimum missing input and keep the clarification non-mutating.

Do not stop after a shallow pass. A good growth strategy session usually needs multiple rounds unless the operator arrives with a precise strategy artifact. Treat "under five questions" as suspicious for fuzzy intent: before concluding, check whether you are merely accepting labels instead of understanding the market, motion, offer, and acquisition system.

Stay in clarification mode until you have a working model of the context and topic. Do not pivot into recording, campaign planning, branch planning, tooling, or Paperclip mutation just because the operator answered the first few questions.

Keep grilling until each required area has either a resolved answer, known source to inspect, or explicit open question:

- acquisition outcome
- durable company goal
- inbound and outbound team goals
- expertise, vertical, channel, or motion team goals
- durable channel or motion projects
- time horizon
- market, vertical, ICP, buyer, and persona
- wedge or painful workflow
- inbound role in the strategy
- outbound role in the strategy
- shared proof, source material, and artifact asks
- offer or CTA
- scope
- non-goals
- success signals
- constraints and risks
- required approvals
- validation expectations
- stop conditions
- Paperclip goals, projects, strategy issues, or campaign issues to connect to

Challenge over-broad intent by asking which shared market experiment, channel, or outbound motion must work first.

Minimum bar before summary:

- Ask at least one question about each required area above unless it was already answered clearly.
- Ask follow-up questions when an answer contains vague words like "growth", "acquisition", "inbound", "outbound", "ICP", "vertical", "operators", "founders", "proof", "content", "leads", "walkthroughs", "campaign", "repeatable", or "validation".
- Pressure-test contradictions and missing context: if two answers imply different markets, buyers, offers, channel roles, proof requirements, goals, or stop conditions, ask another question instead of smoothing it over.
- Before summarizing, be able to restate the durable goal shape, market/ICP, painful workflow, inbound role, outbound role, offer/CTA, first concrete market experiment or AFK loop, non-goals, success evidence, and stop conditions.
- Do not produce the final summary while material ambiguity remains in market, ICP, wedge, channel roles, offer, scope, validation, approvals, or stop conditions.

## Question Bank

Use these as prompts, not a script:

- What acquisition outcome should this strategy serve?
- What durable company goal and team goals should anchor the work?
- Which durable channel or motion deserves a project?
- What market, vertical, ICP, buyer, or persona is in scope first?
- What painful workflow or wedge should inbound and outbound both reinforce?
- What should inbound do that outbound should not do?
- What should outbound do that inbound should not do?
- What proof, source material, or artifact ask should both branches share?
- What CTA or next step should the market see?
- What would make this strategy cycle work?
- What should be explicitly out of scope?
- Which Paperclip goal, project, parent issue, or campaign issue should this connect to?
- What must trigger a stop and operator question?

## Output

End with:

```markdown
## Growth Clarification Summary

### Outcome

### Goal Structure

### Projects

### Time Horizon

### Market / Vertical

### ICP / Buyer / Persona

### Wedge Or Painful Workflow

### Inbound Role

### Outbound Role

### Shared Proof And Source Material

### Artifact Ask

### Offer / CTA

### Scope

### Non-Goals

### Success Signals

### Constraints

### Risks

### Required Approvals

### Validation

### Stop Conditions

### Paperclip Connections

### Open Questions
```

Then ask whether to continue into `growth-record-strategy`.

## V1 Boundaries

Out of scope for v1: automatic sending, automatic posting, scheduling, CRM ownership, deliverability infrastructure, analytics dashboards, full revenue attribution, autonomous reply handling, and creating new execution agents.

## Mutation Rule

Never create or update Paperclip goals, projects, issues, approvals, skills, documents, comments, status, or assignments from this skill.
