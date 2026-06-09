# Paperclip Integration Matrix

Paperclip operator skills should choose the narrowest surface that can perform the correct Paperclip-native operation.

## Priority Rule

Use surfaces in this order:

1. **MCP** when a matching `mcp__paperclip` tool exists.
2. **CLI** when the operation is local/setup-oriented or MCP does not expose it.
3. **REST API** when MCP and CLI do not expose a Paperclip-native record or mutation.

Do not degrade the model because the first surface is missing a command. For example, if a strategy needs a Project or keyed `plan` document, use REST rather than embedding everything in an issue description.

## Current MCP Coverage

The currently exposed Paperclip MCP tools may cover:

- Goals: `list_goals`, and sometimes `create_goal` / `update_goal` depending on the runtime.
- Issues: `list_issues`, `get_issue`, `create_issue`, `update_issue`, `comment_on_issue`, `checkout_issue`, `release_issue`, `delete_issue`
- Approvals: `list_approvals`
- Agents: `list_agents`
- Monitoring: `get_dashboard`, `list_activity`

Known MCP gaps:

- no dedicated `list_projects`
- no `create_project`
- no `update_project`
- no keyed issue-document writer such as `PUT /documents/plan`
- no exposed `blockedByIssueIds` create/update field in observed issue tools
- no company skill-library operations
- agents are read-only through the exposed MCP surface

Observed MCP behavior can drift from its schema. In particular, a tool may expose a `parent_issue_id` argument but still return a created issue with `parentId: null`, and a create surface may normalize new issues to `backlog`. Verify created records before trusting parent, project, status, goal, assignee, or blocker links.

`list_goals` may describe itself as listing goals and projects, but observed output can contain only goal-like records. Treat project discovery as REST-required unless the actual response includes project records with stable project ids.

## Operation Matrix

| Operation | Preferred surface | Fallback | Notes |
|---|---|---|---|
| Check active Paperclip company | MCP context | CLI `paperclipai context show --json` | MCP tools target the configured active company. CLI exposes profile details. |
| Derive REST auth | CLI auth store | `PAPERCLIP_API_KEY` env var | Use `paperclipai auth whoami --json` to verify board auth. Stored board credentials live in `~/.paperclip/auth.json`; do not print tokens. |
| List companies | CLI | REST | No current MCP company list tool. |
| Export/import company | CLI | REST if documented | Use CLI for backup/restore workflows. |
| List goals | MCP `list_goals` | REST `GET /api/companies/{companyId}/goals` | Verify response shape before assuming projects are included. |
| Create goal | MCP `create_goal` if exposed and verified | CLI `paperclipai goal create`, REST `POST /api/companies/{companyId}/goals` | Must support `level`, `status`, `parentId`, and `ownerAgentId`; verify the created record. |
| Update goal | MCP `update_goal` if exposed and verified | CLI `paperclipai goal update`, REST `PATCH /api/goals/{goalId}` | Must support `level`, `status`, `parentId`, and `ownerAgentId`; verify the updated record. |
| List projects | REST `GET /api/companies/{companyId}/projects` | MCP only if actual response includes projects | Treat REST as required today. |
| Create project | REST `POST /api/companies/{companyId}/projects` | none | Required for missing planning-chain projects. |
| Update project / link goals | REST `PATCH /api/projects/{projectId}` | none | Use `goalIds` for goal links. |
| List issues | MCP `list_issues` | CLI `paperclipai issue list --json`, REST | MCP is sufficient for most triage/monitoring. |
| Get issue detail | MCP `get_issue` | CLI `paperclipai issue get --json`, REST | Use before triage or planning. |
| Create parent issue | MCP `create_issue` | CLI `paperclipai issue create`, REST | Include `project_id` when known. |
| Create child issue | MCP only after verifying `parent_issue_id` persists | CLI/REST | Create one issue, verify `parentId`, repair if possible, then continue. |
| Update issue lifecycle | MCP `update_issue` | CLI `paperclipai issue update`, REST | Planning leaves issues in `backlog`. Only triage/delegation may move work to `todo` after approval. |
| Write blocker links | REST for `blockedByIssueIds` | MCP/CLI only if the actual tool exposes and verifies the field | Do not replace first-class blockers with comments unless the operator approves degraded mode. |
| Comment on issue | MCP `comment_on_issue` | CLI `paperclipai issue comment`, REST | Use comments for triage reasoning. |
| Checkout/release issue | MCP `checkout_issue` / `release_issue` | CLI/REST | Respect checkout conflict semantics. |
| Delete issue | MCP `delete_issue` | REST | Destructive; require explicit operator approval. |
| Write `plan` document | REST `PUT /api/issues/{issueId}/documents/plan` | issue description fallback only if REST unavailable or rejected | Do not claim CLI/MCP can do this unless a tool appears. |
| List approvals | MCP `list_approvals` | CLI `paperclipai approval list --json`, REST | Monitoring and board-decision workflows. |
| Resolve approvals | CLI or REST if available | none through current MCP | Current exposed MCP list is read-oriented for approvals. |
| List agents | MCP `list_agents` | CLI `paperclipai agent list --json`, REST | Current MCP agent surface is read-only. |
| Create agents / hire agents | REST `POST /api/companies/{companyId}/agent-hires` or `POST /api/companies/{companyId}/agents` | Paperclip UI | Use `paperclip-create-agent`. Inspect org/config/skills first, ask approval, create or submit hire, then verify agent and approval state. |
| Update existing agents | REST/CLI depending operation | Paperclip UI | Use `paperclip-admin`. Inspect current agent and skills first, ask approval, then verify the updated agent. |
| Dashboard summary | MCP `get_dashboard` | CLI `paperclipai dashboard get --json`, REST | Preferred for `paperclip-monitor`. |
| Activity log | MCP `list_activity` | CLI `paperclipai activity list --json`, REST | Preferred for `paperclip-monitor`. |
| Costs | MCP dashboard/cost fields | REST costs API | Use REST for detailed cost drill-down if MCP summary is insufficient. |
| Company skill library | CLI `paperclipai skills ...` | REST skills API | MCP currently lacks skill-library tools. |
| Local CLI setup/auth/context | CLI | none | Use `paperclipai` for local environment work. |

## Skill Guidance

**paperclip-setup**

- Use CLI for local `paperclipai` path, version, context, and company list.
- Use MCP only to verify active-company access when useful.
- Use bundled templates for project docs.

**paperclip-clarify**

- Usually no Paperclip mutation.
- Use MCP/CLI reads only when an answer can be discovered from current Paperclip state.

**paperclip-record-strategy**

- Use MCP for Goal create/update only when the current runtime exposes and correctly persists those fields; otherwise use CLI or REST.
- Use REST for Project list/create/update.
- Use REST for the parent Issue `plan` document.
- Fall back to embedding the plan in the issue description only when REST is unavailable or explicitly rejected.

**paperclip-plan-work**

- Use MCP issue reads.
- Use MCP issue creates only when parent linkage is known to verify for the active tool surface.
- Create and verify one child issue at a time before continuing.
- Create planned issues as `backlog` and unassigned only.
- Do not move issues to `todo`, assign, checkout, or manually invoke heartbeats from planning.
- Verify `parentId`, `projectId`, `goalId`, `status`, null assignee, and `blockedByIssueIds` after each write.
- Use REST for plan-document reads/writes or fields not exposed by MCP/CLI, including blocker links.
- Stop on the first unrepaired structural mismatch and report partial state.

**paperclip-triage**

- Use MCP issue reads/updates/comments.
- Use REST only for fields not exposed by MCP/CLI.
- Recommend first, mutate after approval.
- Triage is the phase that may recommend moving ready backlog issues to `todo`.

**paperclip-monitor**

- Use MCP dashboard, activity, approvals, agents, and issues first.
- Use CLI/REST for deeper drill-down when MCP summaries are insufficient.

**paperclip-admin**

- Use MCP for reads when exposed.
- Use CLI/REST for existing-agent administration, company skill-library changes, assignments, and small record repairs not exposed through MCP.
- Ask before any mutation, especially attaching skills, changing budgets, changing runtimes, or making work startable.
- Verify every changed record after the write.

**paperclip-create-agent**

- Use CLI/MCP reads for context where available, then REST for native agent creation or hire submission.
- Prefer `/agent-hires` when governance is required or board visibility is useful; use direct `/agents` only with explicit operator approval.
- Mirror company conventions from existing agents, org chart, skills, adapter configuration docs, and current agent configuration examples.
- Create managed instructions bundles for local agents instead of durable legacy prompt fields.
- Leave timer heartbeats disabled by default; enable scheduled heartbeats only with explicit justification.
- After creation, verify agent fields and approval state before creating keys, syncing skills, or assigning work. Do not manually invoke another agent's heartbeat; Paperclip agents wake through their own heartbeat policy after eligible assignment.
