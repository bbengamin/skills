---
name: paperclip-admin
description: Handle general Paperclip administration and small operator requests without starting a full planning session. Use when the user asks to check Paperclip state, make a minor control-plane change, create or update a Paperclip agent, inspect or attach company skills, adjust assignments, or perform ad hoc Paperclip maintenance.
---

# Paperclip Admin

Route small Paperclip operator requests through the narrowest safe workflow.

Use this skill for ad hoc Paperclip work that is not primarily clarification, strategy recording, recursive planning, AFK-readiness triage, or execution monitoring. If the request grows into one of those workflows, switch to the dedicated skill and say why.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/paperclip-operator/control-plane.md`
- `../../../docs/paperclip-operator/workflow.md`
- `../../../docs/paperclip-operator/cli-contract.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Request Routing

- Use `paperclip-monitor` for broad read-only health reports across agents, issues, approvals, activity, cost, or blocked work.
- Use `paperclip-clarify` when the operator's desired outcome is fuzzy and needs shaping before any control-plane record is changed.
- Use `paperclip-record-strategy` when the operator wants a new Goal, Project, Parent Issue, or `plan` document.
- Use `paperclip-plan-work` when decomposing a strategy artifact or parent issue into child issues.
- Use `paperclip-triage` when deciding whether issues are ready for AFK execution.
- Use `paperclip-create-agent` when creating or hiring a new Paperclip agent.
- Stay in `paperclip-admin` for narrow reads, minor edits, agent provisioning, company skill-library operations, assignment tweaks, budget/status checks, and one-off maintenance.

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

Prefer MCP tools when exposed; otherwise use `paperclipai` with JSON output:

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

- MCP only if a create/update agent tool is actually exposed.
- `paperclipai` if it exposes the needed agent command.
- REST API if CLI/MCP do not expose the required native fields.
- Paperclip UI as the final fallback when no callable surface can safely create or update agents.

After update, read the agent back and verify name, role, manager, adapter, skills, budget, and heartbeat policy.

## Minor Mutations

Use this skill for small approved changes such as:

- editing an issue title, description, priority, label, assignee, or lifecycle state
- commenting on an issue
- attaching or detaching a company skill from an agent
- adjusting an agent budget or pause/resume setting
- resolving a small Paperclip record mismatch found during inspection
- creating a single simple issue when the operator already knows the exact desired issue

Do not silently turn broad work into `todo`, assign broad issues, checkout work, wake agents, or approve board gates. If a change would make work startable, call out that it crosses into triage or delegation and ask explicitly.

## Mutation Rule

Read freely. Ask before creating, updating, deleting, assigning, checking out, waking, approving, rejecting, installing, or attaching anything in Paperclip.

Destructive changes require especially explicit approval: delete, cancel, budget reduction, credential/runtime change, approval rejection, and agent disable/termination.
