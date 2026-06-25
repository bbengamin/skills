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

Default to project-local MCP configuration. MCP is not required for skills to load; it is only the fallback surface for Paperclip operations that are missing from the CLI or would otherwise require brittle parsing.

For Codex, write Paperclip MCP config to `.codex/config.toml` in the current trusted project unless the operator explicitly asks for a global install. Use global config only after explicit approval and write it to `~/.codex/config.toml`.

Project-local default:

```toml
[mcp_servers.paperclip]
command = "npx"
args = ["-y", "@bbengamin/paperclip-mcp-server"]
```

Global install uses the same table in `~/.codex/config.toml`. Before writing either file, show the target path, the exact TOML table, and whether an existing `mcp_servers.paperclip` entry will be created, replaced, or left unchanged.

For Claude Code, use project-local `.mcp.json` through the Claude CLI:

```sh
claude mcp add paperclip -s project -- npx -y @bbengamin/paperclip-mcp-server
```

This writes the equivalent shared project config:

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

Global or user-level installs are allowed only after explicit approval. Before writing either config, show the target path, the exact TOML table, Claude command, or JSON entry, and whether an existing `paperclip` MCP entry will be created, replaced, or left unchanged.

After writing MCP config, verify the target file contains the expected table and verify the npm package can be resolved:

```sh
npm view @bbengamin/paperclip-mcp-server version
```

Then tell the operator to restart Codex or Claude Code, or start a new thread/session, before expecting Paperclip MCP tools to appear. Do not treat missing MCP tools in the same running thread as install failure unless the restarted session still cannot load them.

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
- no dedicated agent update or agent instructions-bundle tools
- no company skill-library tools
- no secret, plugin, cloud, routine, or worktree tools
- no dedicated wiki or llm-wiki plugin bridge tools
- no documented native `paperclipai` wiki management command
- no dedicated project create/update or goal create/update tools in MCP 0.1.0

Treat write schemas as claims to verify, not proof. After issue creation or update, read the issue back and confirm parent, project, goal, status, blocker links, and execution policy before continuing with dependent mutations.

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

During planning, create issues as `backlog` and unassigned. Do not move planned work to `todo`, assign, attach reviewer gates, checkout, or manually invoke heartbeats. Triage or delegation may make approved work startable by moving it to `todo`, assigning it, attaching required reviewers, or checking it out; Paperclip's heartbeat policy handles agent pickup after assignment.

## Issue Reviewers

The native issue reviewer field is the issue `executionPolicy`, specifically `executionPolicy.stages[].participants` on a stage with `type: "review"`. The UI reviewer control maps to that participant list. Do not write `reviewRequest` when the operator asks to set a reviewer unless you have just verified that the target Paperclip environment maps it to the UI-backed reviewer field.

Common reviewer write:

```json
{
  "executionPolicy": {
    "mode": "normal",
    "commentRequired": true,
    "stages": [
      {
        "type": "review",
        "approvalsNeeded": 1,
        "participants": [
          {
            "type": "agent",
            "agentId": "<reviewer-agent-id>"
          }
        ]
      }
    ]
  }
}
```

Use CLI or dedicated MCP only if the surface can write and verify `executionPolicy`. Otherwise use `paperclipApiRequest` or direct REST:

```text
PATCH /issues/{issueId}
```

with JSON containing the `executionPolicy` object above. After writing, read the issue back and verify:

- `executionPolicy.mode`
- `executionPolicy.commentRequired`
- `executionPolicy.stages[].type`
- `executionPolicy.stages[].approvalsNeeded`
- `executionPolicy.stages[].participants[].type`
- `executionPolicy.stages[].participants[].agentId` or native user id

If the reviewer agent exists but is `status: "error"`, record that the control-plane reviewer assignment is correct but runtime review execution may still be blocked until the agent's runtime error is cleared.

## llm-wiki Reads

There is no documented native `paperclipai` wiki command, and llm-wiki is not exposed under `/api/wiki/...`. Treat public-looking wiki URLs as SPA routes only. For example:

```text
https://your-paperclip-host.example.com/<company-slug>/wiki/page/wiki/sources/rl-30-day-validation-plan.md
```

maps to page path:

```text
wiki/sources/rl-30-day-validation-plan.md
```

Use `paperclip-wiki-fetch` for the request shape, route list, and examples. It reads llm-wiki through plugin bridge routes:

```text
POST /api/plugins/paperclipai.plugin-llm-wiki/data/page-content
POST /api/plugins/paperclipai.plugin-llm-wiki/data/pages
POST /api/plugins/paperclipai.plugin-llm-wiki/data/sources
```

Prefer MCP `paperclipApiRequest` when available because these routes live under `/api` and accept JSON bodies. If MCP is unavailable or broken, use direct REST with bearer auth. Never print bearer tokens, and never substitute `/api/wiki/...` for the plugin bridge route.

## llm-wiki Mutations

Use `paperclip-wiki-manage` for create, update, rename, archive, delete, publish, sync, or other llm-wiki mutations. There is no documented native `paperclipai` wiki management command and no dedicated MCP wiki management tool.

For page writes, use the confirmed plugin action route:

```text
POST /api/plugins/paperclipai.plugin-llm-wiki/actions/write-page
```

It accepts a top-level `params` object with `companyId`, `wikiId`, `spaceSlug`, `path`, `contents`, optional `expectedHash`, and optional `summary`.

For non-page-write mutations, identify a confirmed plugin bridge route and schema under `/api/plugins/paperclipai.plugin-llm-wiki/data/...` or `/api/plugins/paperclipai.plugin-llm-wiki/actions/...` before mutating. Do not infer write routes from read routes, and do not use `/api/wiki/...`. Wiki management must read the target first, show the exact proposed JSON and markdown diff or full body, wait for explicit approval, re-fetch before writing when the target exists, stop on hash/update-time conflicts, write only through the confirmed route, and read back the page or source to verify title, path, body or source metadata, update time, and hash.

## MCP API Request Fallback

`paperclipApiRequest` is the supported fallback when CLI and dedicated MCP tools lack a needed operation. It is limited to paths under `/api` and JSON bodies. Do not silently downgrade the Paperclip model because a tool command is missing.

Common operations that may require `paperclipApiRequest`:

```text
GET  /companies/{companyId}/goals
POST /companies/{companyId}/goals
PATCH /goals/{goalId}
GET  /companies/{companyId}/projects
POST /companies/{companyId}/projects
PATCH /projects/{projectId}
PATCH /issues/{issueId} for native fields not exposed by CLI/MCP
PATCH /issues/{issueId} with executionPolicy for issue reviewers
GET  /agents/{agentId}/instructions-bundle
PATCH /agents/{agentId}/instructions-bundle
GET  /agents/{agentId}/instructions-bundle/file?path=AGENTS.md
PUT  /agents/{agentId}/instructions-bundle/file
DELETE /agents/{agentId}/instructions-bundle/file?path=AGENTS.md
POST /plugins/paperclipai.plugin-llm-wiki/data/page-content
POST /plugins/paperclipai.plugin-llm-wiki/data/pages
POST /plugins/paperclipai.plugin-llm-wiki/data/sources
```

After each API request, read the record back through CLI or MCP and verify the native field changed. Do not rely on a successful response alone.

### Managed Agent Instructions

Some Paperclip versions expose managed agent instructions in the CLI as `paperclipai agent instructions-bundle`, `instructions-bundle:update`, `instructions-file:get`, `instructions-file:put`, and `instructions-file:delete`. The currently installed CLI in an operator environment may still expose only `agent list`, `agent get`, and `agent local-cli`; do not conclude the API lacks support from that CLI help output alone.

Dedicated MCP tools currently read agents but do not expose instructions-bundle commands. Use `paperclipApiRequest` for these `/api` routes when available, then direct REST if MCP is unavailable:

```text
GET    /api/agents/{agentId}/instructions-bundle
PATCH  /api/agents/{agentId}/instructions-bundle
GET    /api/agents/{agentId}/instructions-bundle/file?path=AGENTS.md
PUT    /api/agents/{agentId}/instructions-bundle/file
DELETE /api/agents/{agentId}/instructions-bundle/file?path=AGENTS.md
```

`PATCH /instructions-bundle` updates bundle metadata such as `mode`, `rootPath`, `entryFile`, and `clearLegacyPromptTemplate`. `PUT /instructions-bundle/file` accepts JSON with `path`, `content`, and optional `clearLegacyPromptTemplate`.

Agent instruction writes are behavior-changing mutations. Read the current file first, present the exact proposed diff or no-op verification plan, get approval, write only the approved content, then read back and verify exact content, byte size, bundle `mode`, `entryFile`, and the touched file path. Avoid extraction commands that add or remove final newlines unless that newline change is intentional.

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
GET  /api/companies/{companyId}/goals
POST /api/companies/{companyId}/goals
PATCH /api/goals/{goalId}
GET  /api/companies/{companyId}/projects
POST /api/companies/{companyId}/projects
PATCH /api/projects/{projectId}
PATCH /api/issues/{issueId} for native fields not exposed by CLI/MCP
GET  /api/agents/{agentId}/instructions-bundle
PUT  /api/agents/{agentId}/instructions-bundle/file
```

Prefer the direct record update route for goal updates. `PATCH /api/companies/{companyId}/goals/{goalId}` may not exist even when company-scoped list and create routes do.

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

# Set an agent reviewer through the native execution policy.
curl -sS -X PATCH "$PAPERCLIP_API_BASE/api/issues/$ISSUE_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"executionPolicy":{"mode":"normal","commentRequired":true,"stages":[{"type":"review","approvalsNeeded":1,"participants":[{"type":"agent","agentId":"<reviewer-agent-id>"}]}]}}'

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
