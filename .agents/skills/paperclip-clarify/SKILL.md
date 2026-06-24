---
name: paperclip-clarify
description: Run a non-mutating clarification session before Paperclip planning. Use when the user has fuzzy intent and needs goal, scope, constraints, success criteria, risks, autonomy level, and validation clarified before creating Paperclip records.
---

# Paperclip Clarify

Turn fuzzy operator intent into a structured clarification summary. Do not mutate Paperclip.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/paperclip-operator/workflow.md`
- `references/docs/paperclip-operator/control-plane.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Process

Run this as a Paperclip-specific grilling session.

Walk the decision tree one branch at a time, resolving dependencies before dependent decisions. For example, do not clarify issue scope before the outcome is stable, do not clarify autonomy before the blast radius is known, and do not clarify validation before success criteria are concrete.

Ask exactly one question at a time, wait for the operator's answer, then choose the next highest-leverage branch. For each question, provide your recommended answer so the operator can accept, edit, or reject it quickly. Never bundle multiple questions into one turn.

If the answer can be discovered from the codebase or Paperclip state, inspect that instead of asking.

If the operator provides a Paperclip wiki URL, wiki page path, or captured wiki source as context, use `paperclip-wiki-fetch` to read it before asking questions that the wiki material can answer. If wiki access details are missing, ask for the minimum missing input and keep the clarification non-mutating.

Do not stop after a shallow pass. A good session usually needs multiple rounds unless the input is already unusually precise. Treat "under five questions" as suspicious for fuzzy intent: before concluding, check whether you are merely accepting labels instead of understanding the work.

Maintain a lightweight decision ledger as you go:

- **Established**: facts and decisions that are resolved enough to plan against.
- **Assumptions**: recommended answers the operator has not explicitly confirmed.
- **Open branches**: load-bearing decisions still unresolved.
- **Contradictions**: answers that imply incompatible scope, ownership, validation, autonomy, or stop conditions.

Use the ledger to choose the next question. If an answer resolves one branch but exposes a dependency, follow the dependency before moving laterally.

Stay in clarification mode until you have a working model of the context and topic. Do not pivot into planning, decomposition, implementation, or Paperclip mutation just because the operator answered the first few questions.

Minimum bar before summary:

- Ask at least one question about each required area below unless it was already answered clearly.
- Ask follow-up questions when an answer contains vague words like "safe", "done", "setup", "E2E", "agent", "review", "backend", "frontend", "database", "autonomous", or "self-sufficient".
- Challenge over-broad goals by asking what must be true for the first AFK loop to succeed.
- Test the plan with concrete scenarios: clean checkout, missing secrets, failed E2E, schema change, flaky dependency, blocked agent, partial implementation, and reviewer rejection.
- Pressure-test contradictions and missing context: if two answers imply different scopes, ownership, validation bars, or stop conditions, ask another question instead of smoothing it over.
- Before summarizing, be able to restate the first concrete AFK loop, the control-plane objects it should attach to, what is explicitly out of scope, what evidence proves success, and what must stop the agent.
- Before summarizing, review the decision ledger. Every load-bearing branch must be established, intentionally listed as an open question, or downgraded to a non-blocking assumption.
- Do not produce the final summary while material ambiguity remains in outcome, scope, validation, autonomy, or stop conditions.

Resolve:

- desired outcome
- why it matters
- scope
- non-goals
- success criteria
- target users or operators
- constraints
- risks
- autonomy level
- required approvals
- validation expectations
- stop conditions
- open questions

## Question Bank

Use these as prompts, not as a script. Ask the highest-leverage next question only.

- What exact Paperclip Company, Goal, Project, or existing Issue should this work connect to?
- What result would make the operator say the first AFK loop succeeded?
- What is explicitly out of scope for the first pass?
- Which existing issues are authoritative, and which are historical reference only?
- What can an agent change without asking: frontend, backend, database, infra, docs, tests, secrets, external services?
- What must trigger a stop and board question?
- What validation is mandatory before an issue can be marked done?
- What local setup must be available from a clean checkout?
- Which secrets, services, migrations, seed data, browsers, or test commands are required?
- What failure modes have already happened or are likely?
- What review evidence should the agent leave in comments or artifacts?
- What should happen if the agent cannot run the full validation locally?
- Which decisions are reversible, and which need approval before implementation?
- What would make a planned issue too broad for AFK execution?

## Output

End with a clarification summary:

```markdown
## Clarification Summary

### Outcome

### Why This Matters

### Scope

### Non-Goals

### Success Criteria

### Constraints

### Risks

### Autonomy Level

### Required Approvals

### Validation

### Stop Conditions

### Open Questions
```

Then ask whether to continue into `paperclip-record-strategy`.

## Mutation Rule

Never create or update Paperclip goals, projects, issues, approvals, skills, or comments from this skill.
