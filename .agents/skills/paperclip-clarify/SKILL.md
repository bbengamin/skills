---
name: paperclip-clarify
description: Run a non-mutating clarification session before Paperclip planning. Use when the user has fuzzy intent and needs goal, scope, constraints, success criteria, risks, autonomy level, and validation clarified before creating Paperclip records.
---

# Paperclip Clarify

Turn fuzzy operator intent into a structured clarification summary. Do not mutate Paperclip.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/paperclip-operator/workflow.md`
- `../../../docs/paperclip-operator/control-plane.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Process

Ask one question at a time. For each question, provide your recommended answer.

If the answer can be discovered from the codebase or Paperclip state, inspect that instead of asking.

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
