# Paperclip Integration Contract

Local operator skills operate Paperclip through the best available surface: Paperclip MCP tools, `paperclipai`, then REST API fallback.

## Surface Priority

Prefer surfaces in this order:

1. **Paperclip MCP tools** for supported control-plane operations.
2. **`paperclipai` CLI** for local setup, context, skills, company export/import, and operations not exposed through MCP.
3. **REST API** for Paperclip-native records missing from both MCP and CLI.

Do not silently downgrade the Paperclip model because one surface lacks coverage. If the planning chain needs a Goal, Project, Parent Issue, or `plan` document, use the surface that can create it.

For the full operation-by-operation decision table, read `docs/paperclip-operator/integration-matrix.md`.

## MCP Coverage

Use MCP when available for:

- listing goals: `mcp__paperclip.list_goals`
- creating goals: `mcp__paperclip.create_goal`
- updating goals: `mcp__paperclip.update_goal`
- listing, creating, updating, commenting on, checking out, and releasing issues
- creating child issues with `parent_issue_id`
- attaching issues to projects with `project_id` on issue creation
- listing approvals
- listing agents
- reading dashboard, cost, activity, and issue state

Known MCP gaps:

- project listing is ambiguous; do not rely on `list_goals` returning projects unless the actual response includes project records
- no exposed project create/update tool
- no exposed keyed issue-document writer for `plan`

## Discovery

Before mutating, inspect the current context. With MCP, use the configured active company. With CLI/REST, inspect:

```sh
paperclipai context show --json
paperclipai company list --json
paperclipai dashboard get -C <company-id> --json
```

Prefer the active CLI profile and context. Respect user-provided `--profile`, `--context`, `--api-base`, `--api-key`, and `-C/--company-id`.

## JSON First

Use `--json` whenever the command supports it. If a command lacks JSON output, parse conservatively and report uncertainty.

Common reads:

```sh
paperclipai company list --json
paperclipai agent list -C <company-id> --json
paperclipai issue list -C <company-id> --json
paperclipai issue get <issue-id-or-identifier> --json
paperclipai approval list -C <company-id> --json
paperclipai activity list -C <company-id> --json
paperclipai skills list -C <company-id> --json
```

Common writes:

```sh
paperclipai issue create -C <company-id> --title "..." --description "..." --status backlog
paperclipai issue update <issue-id> --status todo --comment "..."
paperclipai issue comment <issue-id> --body "..."
```

Use CLI when MCP does not expose the needed operation and the CLI does.

## REST Fallback

The Paperclip API is the supported fallback when MCP and CLI lack a needed operation. Do not silently downgrade the Paperclip model because a tool command is missing.

Derive connection details from:

```sh
paperclipai context show --json
```

Use:

- `apiBase` or the active profile API base as the server URL.
- `companyId` or the active profile company id as the company scope.
- the configured API key env var, or `PAPERCLIP_API_KEY`, for bearer auth.

If authentication cannot be derived, ask the operator for the missing credential or ask them to run the relevant `paperclipai auth` or context setup command. Do not create lower-quality artifacts just because REST auth is missing.

Common REST operations not fully covered by MCP/CLI:

```text
GET  /api/companies/{companyId}/projects
POST /api/companies/{companyId}/projects
PATCH /api/projects/{projectId}
PUT  /api/issues/{issueId}/documents/plan
```

For goals and issues, prefer MCP before REST. For projects, treat REST as required for list/create/update unless a future MCP project tool is exposed.

## Approval Boundary

All operator skills must:

1. Inspect current Paperclip state.
2. Present proposed mutations.
3. Wait for operator approval.
4. Apply the approved mutations.
5. Report created/updated records.

Read-only monitoring does not need confirmation.

## Source of Truth

Do not maintain a duplicate local issue ledger. Local files can be drafts, templates, or skill references. Paperclip control-plane state is canonical.
