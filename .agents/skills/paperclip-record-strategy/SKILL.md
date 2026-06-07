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

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Process

1. Confirm there is an approved clarification summary.
2. Inspect current Paperclip context and company.
3. List existing goals and projects. Use the REST API if the CLI does not expose goals or projects.
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

## REST Fallbacks

The CLI is preferred for commands it supports. Missing CLI coverage is not a reason to skip Paperclip-native records when the API supports them.

Use the API for:

- listing goals: `GET /api/companies/{companyId}/goals`
- creating goals: `POST /api/companies/{companyId}/goals`
- listing projects: `GET /api/companies/{companyId}/projects`
- creating projects: `POST /api/companies/{companyId}/projects`
- updating projects with `goalIds`: `PATCH /api/projects/{projectId}`
- writing the parent issue `plan` document: `PUT /api/issues/{issueId}/documents/plan`

Before calling REST, derive `apiBase`, `companyId`, and authentication from `paperclipai context show --json` and the active profile. If auth cannot be derived, stop and ask the operator for the required context instead of degrading the strategy artifact.

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

If the CLI cannot write keyed documents, use the Paperclip API and explain the endpoint used. Only embed the plan in the parent issue description as a last resort after API access is unavailable or explicitly rejected by the operator.

## Mutation Rule

Always present the proposed Goal, Project, Parent Issue, and plan body before creating or updating Paperclip.
