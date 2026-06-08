# Paperclip Integration Contract

Local operator skills operate Paperclip through the best available surface: Paperclip MCP tools, `paperclipai`, then REST API fallback.

## Surface Priority

Prefer surfaces in this order:

1. **Paperclip MCP tools** for supported control-plane operations.
2. **`paperclipai` CLI** for local setup, context, skills, company export/import, and operations not exposed through MCP.
3. **REST API** for Paperclip-native records missing from both MCP and CLI.

Do not silently downgrade the Paperclip model because one surface lacks coverage. If the planning chain needs a Goal, Project, Parent Issue, or `plan` document, use the surface that can create it.

For the full operation-by-operation decision table, read `docs/paperclip-operator/integration-matrix.md`.

## Fresh Environment Setup

The Paperclip CLI executable is `paperclipai`. On a new environment, install it from npm:

```sh
npm install -g paperclipai
```

Verify the install before running operator workflows:

```sh
command -v paperclipai
paperclipai --version
paperclipai context show --json
```

If `paperclipai` is not found after install, check npm's global binary directory:

```sh
npm bin -g
```

Add that directory to `PATH`, then rerun verification. After the CLI is available, authenticate and select/confirm company context:

```sh
paperclipai auth login
paperclipai company list --json
paperclipai context show --json
```

Setup is not finished just because `paperclipai` is installed. Continue until the ladder is resolved:

- CLI installed and on `PATH`
- CLI context readable
- API base reachable
- auth configured
- company context selected

If `paperclipai context show --json` reports the default API base `http://localhost:3100`, verify the local API before interpreting company/auth failures:

```sh
curl -fsS http://localhost:3100/api/health
```

If the health check fails, report that install is complete but the Paperclip API server is not reachable. Ask whether to start the local Paperclip API or switch the CLI context/profile to a different API base. Do not treat this as an auth failure until the API is reachable.

If the CLI has no API base, an empty profile config, or only an unreachable default, ask the operator for the Paperclip environment URL before attempting auth or company commands. Verify the provided URL first:

```sh
curl -fsS <api-base>/api/health
```

After the URL is reachable, ask for approval before writing CLI context:

```sh
paperclipai context set --api-base <api-base> --use
```

For a named or isolated profile, include `--profile <name>`. Then authenticate against that environment:

```sh
paperclipai auth login --api-base <api-base>
paperclipai company list --json
paperclipai context show --json
```

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
- no observed create/update field for `blockedByIssueIds`
- observed issue create may accept `parent_issue_id` while returning `parentId: null`; verify and repair parent links before continuing

Treat write schemas as claims to verify, not proof. After issue creation or update, read the issue back and confirm parent, project, goal, status, and blocker links before continuing with dependent mutations.

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
paperclipai issue update <issue-id> --parent-id <parent-issue-id>
paperclipai issue comment <issue-id> --body "..."
```

Use CLI when MCP does not expose the needed operation and the CLI does.

During planning, create issues as `backlog` and unassigned. Do not move planned work to `todo`, assign, checkout, or manually invoke heartbeats. Triage or delegation may make approved work startable by moving it to `todo`, assigning it, or checking it out; Paperclip's heartbeat policy handles agent pickup after assignment.

## REST Fallback

The Paperclip API is the supported fallback when MCP and CLI lack a needed operation. Do not silently downgrade the Paperclip model because a tool command is missing.

Derive connection details from:

```sh
paperclipai context show --json
paperclipai auth whoami --json
```

Use:

- `apiBase` or the active profile API base as the server URL.
- `companyId` or the active profile company id as the company scope.
- the configured API key env var, or `PAPERCLIP_API_KEY`, for bearer auth.
- the stored board credential in `~/.paperclip/auth.json` when `auth whoami` reports `source: "board_key"` and no API key env var is configured.

Never print bearer tokens in chat or logs. If a token must be exported for REST tooling, show commands that assign it to an environment variable without echoing the value.

If authentication cannot be derived, ask the operator for the missing credential or ask them to run the relevant `paperclipai auth` or context setup command. Do not create lower-quality artifacts just because REST auth is missing.

Common REST operations not fully covered by MCP/CLI:

```text
GET  /api/companies/{companyId}/projects
POST /api/companies/{companyId}/projects
PATCH /api/projects/{projectId}
PUT  /api/issues/{issueId}/documents/plan
PATCH /api/issues/{issueId} for native fields not exposed by MCP/CLI
```

Concrete fallback snippets:

```sh
# Link a project to one or more goals.
curl -sS -X PATCH "$PAPERCLIP_API_BASE/api/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"goalIds":["<goal-id>"]}'

# Write the parent issue plan document.
curl -sS -X PUT "$PAPERCLIP_API_BASE/api/issues/$ISSUE_ID/documents/plan" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: text/markdown" \
  --data-binary @plan.md

# Patch first-class blockers.
curl -sS -X PATCH "$PAPERCLIP_API_BASE/api/issues/$ISSUE_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"blockedByIssueIds":["<blocking-issue-id>"]}'

# Clear an accidental assignee after planning.
curl -sS -X PATCH "$PAPERCLIP_API_BASE/api/issues/$ISSUE_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"assigneeId":null}'
```

After each REST or CLI repair, read the record back and verify the native field changed. Do not rely on a successful HTTP status or command exit alone.

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
