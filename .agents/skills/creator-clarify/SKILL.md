---
name: creator-clarify
description: Run a non-mutating Creator Growth clarification session from rough operator intent into creator, channel, time-period, campaign, and strategy context. Use when planning or revising creator-led distribution, personal-brand strategy, LinkedIn/content campaigns, or creator growth work before creating Paperclip records.
---

# Creator Clarify

Turn rough creator-growth intent into a structured clarification summary. Do not mutate Paperclip.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/creator-operator/workflow.md`
- `references/docs/creator-operator/control-plane.md`

Open Paperclip operator references only when Paperclip lifecycle or mutation rules are needed:

- `references/docs/paperclip-operator/control-plane.md`
- `references/docs/paperclip-operator/workflow.md`

## Process

Ask one question at a time. For each question, provide your recommended answer.

If the answer can be discovered from the repo or Paperclip state, inspect that instead of asking.

If the operator provides a Paperclip wiki URL, wiki page path, or captured wiki source as source material, use `paperclip-wiki-fetch` to read it before asking questions that the wiki material can answer. If wiki access details are missing, ask for the minimum missing input and keep the clarification non-mutating.

Do not stop after a shallow pass. A good creator-growth session usually needs multiple rounds unless the operator arrives with a precise strategy artifact. Treat "under five questions" as suspicious for fuzzy intent: before concluding, check whether you are merely accepting labels instead of understanding the creator, audience, channel, and commercial context.

Stay in clarification mode until you have a working model of the context and topic. Do not pivot into campaign planning, backlog decomposition, publishing ideas, or Paperclip mutation just because the operator answered the first few questions.

Keep grilling until each required area has either a resolved answer, known source to inspect, or explicit open question:

- creator/persona
- desired outcome
- time horizon
- channel(s)
- audience or ICP
- business, market, or content hypothesis
- positioning, story, and expertise to reinforce
- source material and approved inputs
- scope
- non-goals
- success signals
- constraints and risks
- required approvals
- validation expectations
- stop conditions
- Paperclip goals, project, strategy issue, or campaign issue to connect to

Challenge over-broad intent by asking what must be true for the first AFK loop to succeed.

Minimum bar before summary:

- Ask at least one question about each required area above unless it was already answered clearly.
- Ask follow-up questions when an answer contains vague words like "brand", "content", "audience", "ICP", "founders", "operators", "trust", "growth", "campaign", "good posts", "strategy", or "thought leadership".
- Pressure-test contradictions and missing context: if two answers imply different audiences, channels, source material, offers, approvals, or success signals, ask another question instead of smoothing it over.
- Before summarizing, be able to restate the creator/persona, time horizon, audience, channel role, source material, first concrete AFK loop, non-goals, success evidence, and stop conditions.
- Do not produce the final summary while material ambiguity remains in audience, channel, source material, scope, validation, approvals, or stop conditions.

## Question Bank

Use these as prompts, not a script:

- Which creator/persona is this for?
- What time horizon are we planning or revising: year, quarter, month, campaign, or one work item?
- Which channel is in scope first, and which channels should be considered but not planned yet?
- What market, product, or content hypothesis should this test?
- What audience or ICP should the content reach?
- What source material can agents rely on?
- What story, expertise, or positioning must be reinforced?
- What would make the operator say this strategy cycle worked?
- What should be explicitly out of scope?
- Which Paperclip goal, project, parent issue, or campaign issue should this connect to?
- What is too broad for one AFK loop?
- What must trigger a stop and operator question?

## Output

End with:

```markdown
## Creator Clarification Summary

### Outcome

### Creator/Persona

### Time Horizon

### Channels

### Audience/ICP

### Hypothesis

### Positioning And Story

### Source Material

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

Then ask whether to continue into `creator-record-strategy`.

## V1 Boundaries

Out of scope for v1: voice/video/avatar cloning, automatic posting, scheduling, publishing tool selection, analytics dashboard integrations, CRM ownership, full business experiment tracking, and creating creator-execution agents.

## Mutation Rule

Never create or update Paperclip goals, projects, issues, approvals, skills, documents, comments, or assignments from this skill.
