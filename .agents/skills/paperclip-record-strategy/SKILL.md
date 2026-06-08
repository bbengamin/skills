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
- `../../../docs/paperclip-operator/integration-matrix.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Process

1. Confirm there is an approved clarification summary.
2. Inspect current Paperclip context and company.
3. List existing goals and projects. Prefer MCP for goals. Treat project list/create/update as REST-required unless an actual MCP project tool is available.
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

## Surface Rules

Read `integration-matrix.md` before choosing tools.

For this skill:

- Use MCP for Goal create/update and parent Issue create.
- Treat Project list/create/update as REST-required unless a real MCP project tool is available.
- Use REST for the parent Issue `plan` document.
- Do not assume `mcp__paperclip.list_goals` returns projects. If the actual response lacks project records, use REST for project discovery.

Run a REST auth preflight before the first REST mutation:

1. Derive `apiBase` and `companyId` from MCP context if available, then `paperclipai context show --json`.
2. Run `paperclipai auth whoami --json` to confirm the active auth source.
3. If needed, read the stored board credential shape from `~/.paperclip/auth.json`.
4. Confirm the target endpoint is reachable with a read request before writing.

Never print bearer tokens. If auth cannot be derived, stop and ask the operator for the required context instead of degrading the strategy artifact.

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

If MCP/CLI cannot write keyed documents, use the Paperclip API and explain the endpoint used. Only embed the plan in the parent issue description as a last resort after API access is unavailable or explicitly rejected by the operator.

## Mutation Rule

Always present the proposed Goal, Project, Parent Issue, and plan body before creating or updating Paperclip.
