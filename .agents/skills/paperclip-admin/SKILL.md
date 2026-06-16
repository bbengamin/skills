---
name: paperclip-admin
description: Handle general Paperclip administration and small operator requests without starting a full planning session. Use when the user asks to check Paperclip state, make a minor control-plane change, create or update a Paperclip agent, inspect or attach company skills, adjust assignments, or perform ad hoc Paperclip maintenance.
---

# Paperclip Admin

Route small Paperclip operator requests through the narrowest safe workflow.

Use this skill for ad hoc Paperclip work that is not primarily clarification, strategy recording, recursive planning, AFK-readiness triage, or execution monitoring. If the request grows into one of those workflows, switch to the dedicated skill and say why.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/paperclip-operator/control-plane.md`
- `references/docs/paperclip-operator/workflow.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Request Routing

- Use `paperclip-monitor` for broad read-only health reports across agents, issues, approvals, activity, cost, or blocked work.
- Use `paperclip-clarify` when the operator's desired outcome is fuzzy and needs shaping before any control-plane record is changed.
- Use `paperclip-record-strategy` when the operator wants a new Goal, Project, Parent Issue, or `plan` document.
- Use `paperclip-plan-work` when decomposing a strategy artifact or parent issue into child issues.
- Use `paperclip-triage` when deciding whether issues are ready for AFK execution.
- Use `paperclip-create-agent` when creating or hiring a new Paperclip agent.
- Use `paperclip-wiki-manage` when the request is to create, update, rename, archive, delete, publish, sync, or otherwise mutate Paperclip llm-wiki content.
- Stay in `paperclip-admin` for narrow reads, minor edits, agent provisioning, company skill-library operations, assignment or reviewer-gate tweaks, budget/status checks, and one-off maintenance.

## Operating Loop

1. Identify the active company and profile.
2. Inspect current Paperclip state before changing anything.
3. Decide whether the request is read-only or mutating.
4. For read-only requests, answer directly with the relevant records and uncertainty.
5. For mutations, present the exact proposed change and wait for approval.
6. Apply only the approved change.
7. Read the changed record back and verify the expected fields.
8. Report what changed, record ids, and anything that still needs attention.

## Common Reads

Prefer `paperclipai` with JSON output when it supports the read. Use MCP reads when CLI output is insufficient or unavailable:

```sh
paperclipai context show --json
paperclipai company list --json
paperclipai agent list -C <company-id> --json
paperclipai skills list -C <company-id> --json
paperclipai issue list -C <company-id> --json
paperclipai approval list -C <company-id> --json
paperclipai activity list -C <company-id> --json
```

## Agent Administration

Creating a new Paperclip agent belongs in `paperclip-create-agent`. Stay in this skill only for inspecting existing agents or making minor approved updates to an already-created agent.

Before proposing an existing-agent mutation:

1. List existing agents and company skills.
2. Identify the affected agent's current role, manager, adapter/runtime, budget, heartbeat policy, and attached skills.
3. Check whether the requested change should be a new hire instead.
4. Verify any referenced skills exist in the company skill library or propose installing them first.
5. Present the proposed update for approval.

After approval, use the best available surface:

- `paperclipai` if it exposes the needed agent command and verifies the native fields.
- MCP if a create/update agent tool is exposed or MCP reads are needed for context.
- `paperclipApiRequest` if CLI and dedicated MCP tools do not expose the required native fields.
- Direct REST API if CLI and MCP are unavailable or broken.
- Paperclip UI as the final fallback when no callable surface can safely create or update agents.

After update, read the agent back and verify name, role, manager, adapter, skills, budget, and heartbeat policy.

For managed instruction bundle reads/writes, do not rely only on `paperclipai agent --help`: some installed CLI versions expose only `list`, `get`, and `local-cli` even though the REST API supports instructions bundles. Dedicated MCP currently has no instructions-bundle tool. After approval, use `paperclipApiRequest` or direct REST for:

- `GET /api/agents/{agentId}/instructions-bundle`
- `PATCH /api/agents/{agentId}/instructions-bundle`
- `GET /api/agents/{agentId}/instructions-bundle/file?path=AGENTS.md`
- `PUT /api/agents/{agentId}/instructions-bundle/file`
- `DELETE /api/agents/{agentId}/instructions-bundle/file?path=...`

Before writing instructions, read the current file, present the exact diff or no-op verification plan, and get approval. After writing, read back and verify exact content, byte size, bundle mode, entry file, and touched file path. Be careful not to add or remove final newlines unless that is part of the approved change.

## Minor Mutations

Use this skill for small approved changes such as:

- editing an issue title, description, priority, label, assignee, or lifecycle state
- setting or clearing an issue reviewer gate through `executionPolicy.stages[].participants`
- commenting on an issue
- attaching or detaching a company skill from an agent
- reading or updating a managed agent instructions bundle after explicit approval
- adjusting an agent budget or pause/resume setting
- resolving a small Paperclip record mismatch found during inspection
- creating a single simple issue when the operator already knows the exact desired issue

Do not silently turn broad work into `todo`, assign broad issues, attach reviewer gates to broad issues, checkout work, manually invoke heartbeats, approve board gates, or mutate wiki content. If a change would make work startable or change llm-wiki content, call out that it crosses into triage, delegation, or wiki management and ask explicitly.

## Reviewer Gates

When the operator asks to set an issue reviewer, use Paperclip's native issue execution policy:

- write `executionPolicy.stages[].participants` on a stage with `type: "review"`
- include `approvalsNeeded` for the review stage
- include `commentRequired: true` when reviewer comments are required
- do not write `reviewRequest` unless the target environment has just been verified to map it to the UI reviewer field

After writing, read the issue back and verify the reviewer participant is present. If the selected reviewer agent has `status: "error"`, report that assignment is correct but runtime review execution may still need the agent error cleared.

## Mutation Rule

Read freely. Ask before creating, updating, deleting, assigning, checking out, approving, rejecting, installing, or attaching anything in Paperclip. Do not manually invoke another agent's heartbeat; Paperclip rejects cross-agent heartbeat invocation and eligible assignment is enough for the agent's own heartbeat loop to pick up work.

Destructive changes require especially explicit approval: delete, cancel, budget reduction, credential/runtime change, approval rejection, and agent disable/termination.
