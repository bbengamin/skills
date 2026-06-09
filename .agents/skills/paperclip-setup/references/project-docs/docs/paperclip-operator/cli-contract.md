# Paperclip Integration Contract

Local operator skills operate Paperclip through the best available surface: `paperclipai`, Paperclip MCP tools, MCP API requests, then direct REST API fallback.

## Surface Priority

Prefer surfaces in this order:

1. **`paperclipai` CLI** when it supports the exact operation and can verify it cleanly, preferably with `--json`.
2. **Paperclip MCP tools** when CLI lacks the operation, lacks a required field, or would require brittle output parsing.
3. **MCP `paperclipApiRequest`** for Paperclip-native records missing from both CLI and dedicated MCP tools.
4. **Direct REST API** only when CLI and MCP are unavailable or broken.

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
paperclipai context show --json
paperclipai context set --api-base <api-base> --use
```

For a named or isolated profile, include `--profile <name>`. Treat `context set` as replacing the profile's configured values rather than merging unknown existing fields. Once a company is known, preserve the API base by setting both values together:

```sh
paperclipai context set --api-base <api-base> --company-id <company-id> --use
paperclipai context show --json
```

Verify the resulting profile contains both `apiBase` and `companyId`. Then authenticate against that environment:

```sh
paperclipai auth login --api-base <api-base>
paperclipai company list --json
paperclipai context show --json
```

## MCP Coverage

Use the `@bbengamin/paperclip-mcp-server` package when MCP fallback is needed. The server is configured with:

```sh
npx -y @bbengamin/paperclip-mcp-server
```

Token-free MCP host config can rely on the active CLI profile:

```json
{
  "mcpServers": {
    "paperclip": {
      "command": "npx",
      "args": ["-y", "@bbengamin/paperclip-mcp-server"]
    }
  }
}
```

The server reads explicit `PAPERCLIP_API_URL`, `PAPERCLIP_API_KEY`, and `PAPERCLIP_COMPANY_ID` first. If those are absent, it falls back to context from `~/.paperclip/context.json` or `PAPERCLIP_CONTEXT`, and board auth from `~/.paperclip/auth.json` or `PAPERCLIP_AUTH_STORE`.

### MCP Install Scope

Default to project-local MCP configuration. Write Paperclip MCP config to `.codex/config.toml` in the current trusted project unless the operator explicitly asks for a global install. Use global config only after explicit approval and write it to `~/.codex/config.toml`.

Project-local default:

```toml
[mcp_servers.paperclip]
command = "npx"
args = ["-y", "@bbengamin/paperclip-mcp-server"]
```

Global install uses the same table in `~/.codex/config.toml`. Before writing either file, show the target path, the exact TOML table, and whether an existing `mcp_servers.paperclip` entry will be created, replaced, or left unchanged.

After writing MCP config, verify the target file contains the expected table and verify the npm package can be resolved:

```sh
npm view @bbengamin/paperclip-mcp-server version
```

Then tell the operator to restart Codex or start a new thread before expecting Paperclip MCP tools to appear. Do not treat missing MCP tools in the same running thread as install failure unless the restarted session still cannot load them.

Dedicated MCP read tools:

- `paperclipMe`
- `paperclipInboxLite`
- `paperclipListAgents`
- `paperclipGetAgent`
- `paperclipListIssues`
- `paperclipGetIssue`
- `paperclipGetHeartbeatContext`
- `paperclipListComments`
- `paperclipGetComment`
- `paperclipListIssueApprovals`
- `paperclipListDocuments`
- `paperclipGetDocument`
- `paperclipListDocumentRevisions`
- `paperclipListProjects`
- `paperclipGetProject`
- `paperclipGetIssueWorkspaceRuntime`
- `paperclipWaitForIssueWorkspaceService`
- `paperclipListGoals`
- `paperclipGetGoal`
- `paperclipListApprovals`
- `paperclipGetApproval`
- `paperclipGetApprovalIssues`
- `paperclipListApprovalComments`

Dedicated MCP write tools:

- `paperclipCreateIssue`
- `paperclipUpdateIssue`
- `paperclipCheckoutIssue`
- `paperclipReleaseIssue`
- `paperclipAddComment`
- `paperclipSuggestTasks`
- `paperclipAskUserQuestions`
- `paperclipRequestConfirmation`
- `paperclipRequestCheckboxConfirmation`
- `paperclipUpsertIssueDocument`
- `paperclipRestoreIssueDocumentRevision`
- `paperclipControlIssueWorkspaceServices`
- `paperclipCreateApproval`
- `paperclipLinkIssueApproval`
- `paperclipUnlinkIssueApproval`
- `paperclipApprovalDecision`
- `paperclipAddApprovalComment`

Escape hatch:

- `paperclipApiRequest`

Known MCP gaps:

- no dedicated company list/export/import tools
- no company skill-library tools
- no secret, plugin, cloud, routine, or worktree tools
- no dedicated project create/update or goal create/update tools in MCP 0.1.0

Treat write schemas as claims to verify, not proof. After issue creation or update, read the issue back and confirm parent, project, goal, status, and blocker links before continuing with dependent mutations.

## Discovery

Before mutating, inspect the current context:

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

## MCP API Request Fallback

`paperclipApiRequest` is the supported fallback when CLI and dedicated MCP tools lack a needed operation. It is limited to paths under `/api` and JSON bodies. Do not silently downgrade the Paperclip model because a tool command is missing.

Common operations that may require `paperclipApiRequest`:

```text
GET  /companies/{companyId}/projects
POST /companies/{companyId}/projects
PATCH /projects/{projectId}
POST /companies/{companyId}/goals
PATCH /goals/{goalId}
PATCH /issues/{issueId} for native fields not exposed by CLI/MCP
```

After each API request, read the record back through CLI or MCP and verify the native field changed. Do not rely on a successful response alone.

## Direct REST Fallback

Use direct REST only when CLI and MCP are unavailable or broken. Prefer `paperclipApiRequest` from an installed MCP server before shelling out to `curl`.

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

Common direct REST operations mirror the MCP API request paths under `/api`:

```text
GET  /api/companies/{companyId}/projects
POST /api/companies/{companyId}/projects
PATCH /api/projects/{projectId}
POST /api/companies/{companyId}/goals
PATCH /api/goals/{goalId}
PATCH /api/issues/{issueId} for native fields not exposed by CLI/MCP
```

Concrete fallback snippets:

```sh
# Link a project to one or more goals.
curl -sS -X PATCH "$PAPERCLIP_API_BASE/api/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"goalIds":["<goal-id>"]}'

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

After each REST, API request, MCP, or CLI repair, read the record back and verify the native field changed. Do not rely on a successful HTTP status, tool response, or command exit alone.

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
