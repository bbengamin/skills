---
name: paperclip-create-agent
description: Create or hire Paperclip agents using the native governance-aware workflow. Use when the user asks to create, hire, provision, draft, or configure a new Paperclip agent, including choosing role, reporting line, adapter config, desired skills, instructions bundle, budget, heartbeat settings, and approval handling.
---

# Paperclip Create Agent

Create new Paperclip agents by mirroring Paperclip's native hire workflow.

This is a mutating local operator skill. Inspect freely, but do not create an agent, submit a hire request, create keys, attach skills, or change permissions until the operator approves the exact proposal.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/paperclip-operator/control-plane.md`
- `../../../docs/paperclip-operator/workflow.md`
- `../../../docs/paperclip-operator/cli-contract.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

Useful upstream surfaces discovered from Paperclip docs/source:

- `GET /api/companies/{companyId}/agents`
- `GET /api/companies/{companyId}/org`
- `GET /api/companies/{companyId}/agent-configurations`
- `GET /api/companies/{companyId}/skills`
- `GET /llms/agent-configuration.txt`
- `GET /llms/agent-configuration/{adapterType}.txt`
- `GET /llms/agent-icons.txt`
- `POST /api/companies/{companyId}/agent-hires`
- `POST /api/companies/{companyId}/agents`
- `POST /api/agents/{agentId}/keys`
- `POST /api/agents/{agentId}/skills/sync`

## Workflow

1. Confirm context.

   Read CLI context and active company. Verify board access or agent permission to create agents. If the current identity cannot create agents, prepare a hire proposal or approval request instead of attempting creation.

2. Inspect company conventions.

   Read existing agents, org chart, company skills, and agent configurations. Note naming, icons, reporting lines, adapter types, models, environment bindings, default environments, budget conventions, heartbeat defaults, and required Paperclip skills.

3. Choose the route.

   - Use `POST /api/companies/{companyId}/agent-hires` when governance is required, the request came from another agent or issue, or the operator wants a board-visible hire flow.
   - Use `POST /api/companies/{companyId}/agents` only when the operator explicitly approves direct creation and company policy allows it.
   - Use the Paperclip UI as the fallback if no authenticated callable surface can safely create the record.

4. Draft the agent.

   Include `name`, `role`, `title`, `icon`, `reportsTo`, `capabilities`, `adapterType`, `adapterConfig`, `desiredSkills`, managed `instructionsBundle`, `runtimeConfig.heartbeat`, `defaultEnvironmentId`, `budgetMonthlyCents`, explicit `permissions`, and `sourceIssueId`/`sourceIssueIds` when the hire came from Paperclip work.

5. Draft instructions.

   Prefer a role-specific or adjacent Paperclip template when available. Otherwise write a compact `AGENTS.md` covering identity, reporting line, role charter, operating workflow, domain lenses, output bar, collaboration, safety/permissions, and done criteria.

   For execution-heavy agents, include this contract: start actionable work in the same heartbeat; do not stop at a plan unless planning was requested; leave durable progress with a clear next action; use child issues for long or parallel delegated work instead of polling; mark blocked work with owner and action; respect budget, pause/cancel, approval gates, and company boundaries.

6. Review before approval.

   Check for duplicate agents, missing manager, wrong role, unsupported adapter/model, missing skills, plain-text secrets, broad permissions, unnecessary timer heartbeat, vague capabilities, and instructions that conflict with Paperclip source-of-truth rules.

7. Ask for operator approval.

   Show the proposed route, payload summary, manager, adapter/model, skills, permissions, budget, heartbeat policy, environment, source issue linkage, and any risky settings. Wait for approval.

8. Apply and verify.

   Create the hire or agent with REST/API surface. Read the resulting agent and approval back. Verify status:

   - `pending_approval` with a `hire_agent` approval when governance applies
   - `idle` or company default active state when direct creation succeeds

   Confirm persisted fields: name, role, reportsTo, adapter type/config, desired skills, instructions bundle mode/path, heartbeat config, budget, permissions, environment, and source linkage.

9. Set up local CLI only after creation is valid.

   For runnable local agents, use:

   ```sh
   paperclipai agent local-cli <agentRef> -C <company-id> --json
   ```

   Never print long-lived API keys in chat. Summarize key creation and tell the operator where the command emitted exports if needed.

10. Report outcome.

   Include agent id/url key, approval id if any, status, manager, adapter, skills, heartbeat state, budget, and next operator action.

## Payload Notes

Valid roles in current Paperclip source include `ceo`, `cto`, `cmo`, `cfo`, `security`, `engineer`, `designer`, `pm`, `qa`, `devops`, `researcher`, and `general`.

Known adapter types include `process`, `http`, `acpx_local`, `claude_local`, `codex_local`, `cursor_cloud`, `gemini_local`, `opencode_local`, `pi_local`, `cursor`, and `openclaw_gateway`.

For `codex_local`, prefer managed instructions over legacy prompt fields. Typical adapter config includes `cwd`, `model`, `env`, `timeoutSec`, `graceSec`, `fastMode`, and only explicitly approved sandbox/approval bypass settings.

## Mutation Rule

Ask before creating hires, creating direct agents, attaching desired skills, creating API keys, changing permissions, setting secrets/env bindings, enabling timer heartbeats, or assigning work. Do not manually invoke another agent's heartbeat; Paperclip agents wake through their own heartbeat policy after eligible assignment.
