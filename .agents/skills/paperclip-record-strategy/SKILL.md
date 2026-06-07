---
name: paperclip-record-strategy
description: Record clarified intent into Paperclip as a planning chain. Use after paperclip-clarify when the operator approves creating or updating the Goal, linked Project, Parent Issue, and plan document.
---

# Paperclip Record Strategy

Create or select the missing Paperclip planning chain:

```text
Goal -> linked Project -> Parent Issue + plan document
```

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/paperclip-operator/control-plane.md`
- `../../../docs/paperclip-operator/workflow.md`
- `../../../docs/paperclip-operator/cli-contract.md`

## Process

1. Confirm there is an approved clarification summary.
2. Inspect current Paperclip context and company.
3. List existing goals and projects when possible.
4. Decide with the operator whether this is:
   - a new goal
   - an existing goal
   - a new project under an existing goal
   - an existing project
   - a new parent issue under an existing project
5. Draft the proposed planning chain.
6. Ask for approval before mutating Paperclip.
7. Create or update only the approved missing parts.
8. Report the resulting Goal, Project, Parent Issue, and plan document link or identifier.

## Strategy Plan Document

Use a parent issue `plan` document for the strategy artifact when supported.

Recommended plan shape:

```markdown
## Outcome

## Why This Matters

## Success Criteria

## Scope

## Non-Goals

## Constraints

## Risks

## Autonomy Level

## Validation

## Stop Conditions

## Planning Notes
```

If the CLI cannot write keyed documents, use the Paperclip API and explain the endpoint used. If neither is available, create the parent issue with the plan in the description and explicitly note that this is a fallback.

## Mutation Rule

Always present the proposed Goal, Project, Parent Issue, and plan body before creating or updating Paperclip.
