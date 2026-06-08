---
name: growth-clarify
description: Run a non-mutating Growth Operator clarification session for acquisition strategy that may span inbound and outbound. Use when planning repeatable acquisition, aligning creator/inbound and outbound strategy, defining growth goals/sub-goals, or choosing durable channel/motion projects before creating Paperclip records.
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

Keep grilling until each required area has either a resolved answer, known source to inspect, or explicit open question:

- acquisition outcome
- durable top-level goal
- inbound and outbound sub-goals
- expertise, vertical, channel, or motion sub-goals
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

## Question Bank

Use these as prompts, not a script:

- What acquisition outcome should this strategy serve?
- What durable goal and sub-goals should anchor the work?
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
