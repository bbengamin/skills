---
name: paperclip-record-strategy
description: Record clarified intent into Paperclip as a planning chain. Use after paperclip-clarify when the operator approves creating or updating the Goal, linked Project, Parent Issue, and plan document.
---

# Paperclip Record Strategy

Create or select the missing Paperclip planning chain:

```text
Goal tree -> linked Project -> Parent Issue + plan document
```

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/paperclip-operator/control-plane.md`
- `references/docs/paperclip-operator/workflow.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Process

1. Confirm there is an approved clarification summary.
2. Inspect current Paperclip context and company.
3. List existing goals and projects using the CLI-first ladder in `integration-matrix.md`.
4. Decide with the operator whether this is:
   - a new root goal or child goal
   - an existing goal
   - a new project under an existing goal
   - an existing project
   - a new parent issue under an existing project
5. Draft the proposed planning chain.
6. Ask for approval before mutating Paperclip.
7. Create or update only the approved missing parts.
8. Report the resulting Goal, Project, Parent Issue, and plan document link or identifier.

## Wiki Source Material

When the approved clarification summary or operator prompt references a Paperclip wiki URL, wiki page path, or captured wiki source, use `paperclip-wiki-fetch` before drafting the planning chain or plan document. Record the fetched page title, path, update time, and hash in the plan's source notes when available, then use the markdown body as source material.

If wiki credentials, company scope, wiki id, space slug, or page path are missing and cannot be inferred from Paperclip context, stop and ask for the missing input instead of drafting from an unfetched wiki reference.

If the operator explicitly asks to publish or sync the resulting strategy artifact to wiki, complete the Paperclip planning-chain proposal first, then use `paperclip-wiki-manage` for the wiki mutation. Do not replace the parent issue `plan` document with wiki as the default source of truth.

## Goal Fields

Paperclip goals have native `level`, `status`, `parentId`, and `ownerAgentId` fields. Do not flatten this structure into titles.

Default mapping:

- `company` for a top-level durable company outcome. Prefer an active root company goal when the goal is the company north star.
- `team` for durable team, function, motion, channel, domain, or strategy child goals. Set `parentId` to the parent company or team goal.
- `agent` only when a specific Paperclip agent owns the goal. Set `ownerAgentId`.
- `task` rarely. Prefer Issues for campaigns, months, sprints, lead lists, draft work, and executable tasks.

Every proposed goal mutation must show `title`, `level`, `status`, `parentId`, and `ownerAgentId` before approval.

## Surface Rules

Read `integration-matrix.md` before choosing tools.

For this skill:

- Use CLI first when it supports the exact native field and can verify the result.
- Use dedicated Paperclip MCP tools when CLI lacks the operation or would require brittle parsing.
- Use MCP `paperclipApiRequest` for project create/update, goal create/update, or native fields not exposed by CLI or dedicated MCP tools.
- Use direct REST only when CLI and MCP are unavailable or broken.
- Use keyed issue documents for the parent Issue `plan`; prefer MCP document tools when CLI lacks native document commands.

Before the first MCP API request or direct REST mutation:

1. Derive `apiBase` and `companyId` from `paperclipai context show --json`.
2. Run `paperclipai auth whoami --json` to confirm the active auth source.
3. If needed, inspect the stored board credential shape from `~/.paperclip/auth.json` without printing secrets.
4. Confirm the target read path works before writing.

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

If CLI cannot write keyed documents, use MCP document tools. If no dedicated MCP tool is available, use `paperclipApiRequest` and explain the path used. Only embed the plan in the parent issue description as a last resort after CLI, MCP, and API access are unavailable or explicitly rejected by the operator.

## Mutation Rule

Always present the proposed Goal, Project, Parent Issue, and plan body before creating or updating Paperclip.
