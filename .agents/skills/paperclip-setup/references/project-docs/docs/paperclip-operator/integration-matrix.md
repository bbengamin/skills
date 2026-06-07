# Paperclip Integration Matrix

Paperclip operator skills should choose the narrowest surface that can perform the correct Paperclip-native operation.

## Priority Rule

Use surfaces in this order:

1. **MCP** when a matching `mcp__paperclip` tool exists.
2. **CLI** when the operation is local/setup-oriented or MCP does not expose it.
3. **REST API** when MCP and CLI do not expose a Paperclip-native record or mutation.

Do not degrade the model because the first surface is missing a command. For example, if a strategy needs a Project or keyed `plan` document, use REST rather than embedding everything in an issue description.

## Current MCP Coverage

The currently exposed Paperclip MCP tools cover:

- Goals: `list_goals`, `create_goal`, `update_goal`
- Issues: `list_issues`, `get_issue`, `create_issue`, `update_issue`, `comment_on_issue`, `checkout_issue`, `release_issue`, `delete_issue`
- Approvals: `list_approvals`
- Agents: `list_agents`
- Monitoring: `get_dashboard`, `list_activity`

Known MCP gaps:

- no dedicated `list_projects`
- no `create_project`
- no `update_project`
- no keyed issue-document writer such as `PUT /documents/plan`
- no company skill-library operations
- agents are read-only through the exposed MCP surface

`list_goals` may describe itself as listing goals and projects, but observed output can contain only goal-like records. Treat project discovery as REST-required unless the actual response includes project records with stable project ids.

## Operation Matrix

| Operation | Preferred surface | Fallback | Notes |
|---|---|---|---|
| Check active Paperclip company | MCP context | CLI `paperclipai context show --json` | MCP tools target the configured active company. CLI exposes profile details. |
| List companies | CLI | REST | No current MCP company list tool. |
| Export/import company | CLI | REST if documented | Use CLI for backup/restore workflows. |
| List goals | MCP `list_goals` | REST `GET /api/companies/{companyId}/goals` | Verify response shape before assuming projects are included. |
| Create goal | MCP `create_goal` | REST `POST /api/companies/{companyId}/goals` | Preferred for strategy recording. |
| Update goal | MCP `update_goal` | REST `PATCH /api/goals/{goalId}` | Preferred for strategy refinement. |
| List projects | REST `GET /api/companies/{companyId}/projects` | MCP only if actual response includes projects | Treat REST as required today. |
| Create project | REST `POST /api/companies/{companyId}/projects` | none | Required for missing planning-chain projects. |
| Update project / link goals | REST `PATCH /api/projects/{projectId}` | none | Use `goalIds` for goal links. |
| List issues | MCP `list_issues` | CLI `paperclipai issue list --json`, REST | MCP is sufficient for most triage/monitoring. |
| Get issue detail | MCP `get_issue` | CLI `paperclipai issue get --json`, REST | Use before triage or planning. |
| Create parent issue | MCP `create_issue` | CLI `paperclipai issue create`, REST | Include `project_id` when known. |
| Create child issue | MCP `create_issue` with `parent_issue_id` | CLI/REST | Use one planning level at a time. |
| Update issue lifecycle | MCP `update_issue` | CLI `paperclipai issue update`, REST | Ask for operator approval before mutation. |
| Comment on issue | MCP `comment_on_issue` | CLI `paperclipai issue comment`, REST | Use comments for triage reasoning. |
| Checkout/release issue | MCP `checkout_issue` / `release_issue` | CLI/REST | Respect checkout conflict semantics. |
| Delete issue | MCP `delete_issue` | REST | Destructive; require explicit operator approval. |
| Write `plan` document | REST `PUT /api/issues/{issueId}/documents/plan` | issue description fallback only if REST unavailable or rejected | Do not claim CLI/MCP can do this unless a tool appears. |
| List approvals | MCP `list_approvals` | CLI `paperclipai approval list --json`, REST | Monitoring and board-decision workflows. |
| Resolve approvals | CLI or REST if available | none through current MCP | Current exposed MCP list is read-oriented for approvals. |
| List agents | MCP `list_agents` | CLI `paperclipai agent list --json`, REST | Current MCP agent surface is read-only. |
| Create/update agents | REST/CLI depending operation | Paperclip UI | Not part of initial operator suite except recommendations. |
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

- Use MCP for Goal create/update and parent Issue create.
- Use REST for Project list/create/update.
- Use REST for the parent Issue `plan` document.
- Fall back to embedding the plan in the issue description only when REST is unavailable or explicitly rejected.

**paperclip-plan-work**

- Use MCP issue reads and creates.
- Use `parent_issue_id` for child issues.
- Use REST only for plan-document reads/writes or fields not exposed by MCP/CLI.

**paperclip-triage**

- Use MCP issue reads/updates/comments.
- Use REST only for fields not exposed by MCP/CLI.
- Recommend first, mutate after approval.

**paperclip-monitor**

- Use MCP dashboard, activity, approvals, agents, and issues first.
- Use CLI/REST for deeper drill-down when MCP summaries are insufficient.
