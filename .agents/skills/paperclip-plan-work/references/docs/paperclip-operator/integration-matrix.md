# Paperclip Integration Matrix

Paperclip operator skills should choose the first surface in the ladder that can perform and verify the correct Paperclip-native operation.

## Priority Rule

Use surfaces in this order:

1. **CLI** when `paperclipai` supports the exact operation and can verify it cleanly, preferably with `--json`.
2. **MCP** when the CLI lacks the operation, lacks the required field, or would require brittle output parsing.
3. **MCP API request** through `paperclipApiRequest` when no dedicated MCP tool exists.
4. **REST API** only when CLI and MCP are unavailable or broken.

Do not degrade the model because an earlier surface is missing a command or field. For example, if a strategy needs a Project or keyed `plan` document and the CLI cannot write it natively, use MCP or `paperclipApiRequest` rather than embedding everything in an issue description.

## Current MCP Server

The supported MCP package is `@bbengamin/paperclip-mcp-server`. It is a thin REST-backed MCP wrapper. It reads explicit `PAPERCLIP_API_URL`, `PAPERCLIP_API_KEY`, and `PAPERCLIP_COMPANY_ID` first, then falls back to the active `paperclipai` context and auth store.

Dedicated MCP tools cover:

- Actor and inbox: `paperclipMe`, `paperclipInboxLite`
- Agents: `paperclipListAgents`, `paperclipGetAgent`
- Issues: `paperclipListIssues`, `paperclipGetIssue`, `paperclipCreateIssue`, `paperclipUpdateIssue`, `paperclipCheckoutIssue`, `paperclipReleaseIssue`
- Comments: `paperclipListComments`, `paperclipGetComment`, `paperclipAddComment`
- Issue documents: `paperclipListDocuments`, `paperclipGetDocument`, `paperclipListDocumentRevisions`, `paperclipUpsertIssueDocument`, `paperclipRestoreIssueDocumentRevision`
- Projects: `paperclipListProjects`, `paperclipGetProject`
- Goals: `paperclipListGoals`, `paperclipGetGoal`
- Approvals: `paperclipListApprovals`, `paperclipGetApproval`, `paperclipGetApprovalIssues`, `paperclipListIssueApprovals`, `paperclipCreateApproval`, `paperclipLinkIssueApproval`, `paperclipUnlinkIssueApproval`, `paperclipApprovalDecision`, `paperclipAddApprovalComment`, `paperclipListApprovalComments`
- Agent/user interactions: `paperclipSuggestTasks`, `paperclipAskUserQuestions`, `paperclipRequestConfirmation`, `paperclipRequestCheckboxConfirmation`
- Heartbeat/workspace runtime: `paperclipGetHeartbeatContext`, `paperclipGetIssueWorkspaceRuntime`, `paperclipControlIssueWorkspaceServices`, `paperclipWaitForIssueWorkspaceService`
- Escape hatch: `paperclipApiRequest`

Known MCP gaps:

- no dedicated company list/export/import tools
- no dedicated agent update or agent instructions-bundle tools; use `paperclipApiRequest` or direct REST for managed instruction bundle reads/writes when the CLI lacks the command
- no company skill-library tools
- no secret, plugin, cloud, routine, or worktree tools
- no dedicated wiki or llm-wiki plugin bridge tools; use `paperclip-wiki-fetch` for reads or `paperclip-wiki-manage` for mutations plus `paperclipApiRequest` or direct REST
- no documented native `paperclipai` wiki management command
- no dedicated project create/update tools in the published MCP list; use `paperclipApiRequest` if CLI cannot do the native operation

Treat write schemas as claims to verify, not proof. After every write, read the record back and confirm parent, project, goal, status, assignee, document, approval, blocker, and execution policy fields before continuing with dependent mutations.

## Operation Matrix

| Operation | Preferred surface | Fallback | Notes |
|---|---|---|---|
| Check active Paperclip company | CLI `paperclipai context show --json` | MCP `paperclipMe` / `paperclipListAgents` | MCP tools use explicit env or active CLI context. CLI remains the setup authority. |
| Derive API auth | CLI auth store | `PAPERCLIP_API_KEY` env var | Use `paperclipai auth whoami --json` to verify board auth. Stored board credentials live in `~/.paperclip/auth.json`; do not print tokens. |
| List companies | CLI `paperclipai company list --json` | direct REST | No dedicated MCP company list tool. |
| Export/import company | CLI `paperclipai company export/import` | direct REST if documented | Use CLI for backup/restore workflows. |
| List/get goals | CLI `paperclipai goal list/get --json` | MCP `paperclipListGoals` / `paperclipGetGoal` | Verify response shape before using goal ids in mutations. |
| Create/update goal | CLI `paperclipai goal create/update --json` | `paperclipApiRequest`, then direct REST | Supports `level`, `status`, `parentId`, and `ownerAgentId`; verify the record. |
| List/get projects | CLI `paperclipai project list/get --json` | MCP `paperclipListProjects` / `paperclipGetProject` | Prefer CLI for ordinary project reads. |
| Create project | CLI `paperclipai project create --json` | `paperclipApiRequest`, then direct REST | Supports `goalIds`, lead agent, target date, environment bindings, and execution-workspace policy. |
| Update project / link goals | CLI `paperclipai project update --json` | `paperclipApiRequest`, then direct REST | Use native `goalIds`; `goalId` is deprecated for single-goal compatibility. |
| List issues | CLI `paperclipai issue list --json` | MCP `paperclipListIssues` | MCP supports richer filters; use it when CLI output is insufficient. |
| Get issue detail | CLI `paperclipai issue get --json` | MCP `paperclipGetIssue` | Use before triage or planning. |
| Create parent issue | CLI `paperclipai issue create` if fields verify | MCP `paperclipCreateIssue` | Include project/parent/status fields when known and verify after creation. |
| Create child issue | CLI `paperclipai issue child:create --payload-json ... --json` | MCP `paperclipCreateIssue`, then `paperclipApiRequest` repair | Parent is explicit in the CLI command; create one issue, verify `parentId`, then continue. |
| Update issue lifecycle/fields | CLI `paperclipai issue update` if fields verify | MCP `paperclipUpdateIssue` | Planning leaves issues in `backlog`. Only triage/delegation may move work to `todo` after approval. |
| Write blocker links | CLI if `blockedByIssueIds` verifies | MCP `paperclipUpdateIssue`, then `paperclipApiRequest` | Do not replace first-class blockers with comments unless the operator approves degraded mode. |
| Set issue reviewer gate | CLI or MCP only if `executionPolicy` verifies | `paperclipApiRequest`, then direct REST | The UI reviewer field maps to agent participants on an `executionPolicy` `review` stage. For ordinary human final acceptance, keep the agent reviewer active and use `request_confirmation`; do not add a user approval stage or use `reviewRequest`. |
| Comment on issue | CLI `paperclipai issue comment` | MCP `paperclipAddComment` | Use comments for triage reasoning. |
| Checkout/release issue | CLI `paperclipai issue checkout/release` | MCP `paperclipCheckoutIssue` / `paperclipReleaseIssue` | Respect checkout conflict semantics. |
| Delete issue | CLI `paperclipai issue delete` after explicit approval | direct REST | Destructive; resolve the exact issue and read it before deletion. |
| Read/write `plan` document | CLI `paperclipai issue document:get/put/revisions --json` | MCP `paperclipGetDocument` / `paperclipUpsertIssueDocument` | Use `baseRevisionId` on updates so stale writes return `409`; prefer keyed documents over description fallback. |
| Issue interactions / confirmation | CLI `paperclipai issue interactions` and `interaction:create` | MCP interaction tools | Use `request_confirmation` for ordinary yes/no decisions, plan acceptance, and human final acceptance after agent review. Bind plan confirmation to the exact document revision and use an idempotency key for every decision card. |
| Inspect issue execution | CLI `paperclipai issue runs/live-runs/active-run/recovery-actions --json` | `paperclipApiRequest` | Distinguish queued/running work, process recovery, missing-comment retry, and explicit recovery actions before intervening. Feature-detect newer run-liveness fields. |
| Issue work products | CLI `paperclipai issue work-products` and work-product CRUD | `paperclipApiRequest` | Use for durable produced artifacts when comments/documents are not the right model. |
| List approvals | CLI `paperclipai approval list --json` | MCP `paperclipListApprovals` / `paperclipListIssueApprovals` | Monitoring and board-decision workflows. |
| Resolve approvals | CLI `paperclipai approval approve/reject/request-revision/resubmit` | MCP `paperclipApprovalDecision` | Verify approval status after mutation. |
| List agents | CLI `paperclipai agent list --json` | MCP `paperclipListAgents` | Use CLI for local agent setup commands. |
| Create agents / hire agents | CLI `paperclipai agent create/hire --payload-json ... --json` | `paperclipApiRequest`, then direct REST | Use `paperclip-create-agent`. Inspect org/config/skills first, ask approval, create or submit hire, then verify agent and approval state. |
| Update existing agents | CLI `paperclipai agent update` and lifecycle/config commands | MCP reads, then `paperclipApiRequest` or direct REST | Use `paperclip-admin`. Inspect current agent and skills first, ask approval, then verify the updated agent. |
| Read/update managed agent instructions | CLI `paperclipai agent instructions-bundle`, `instructions-bundle:update`, and `instructions-file:*` | `paperclipApiRequest`, then direct REST | Feature-detect with `paperclipai agent --help`; dedicated MCP has no instructions-bundle tool. Ask approval before writes and read back exact content, size, and entry file. |
| Dashboard summary | CLI `paperclipai dashboard get --json` | MCP if a dedicated/dashboard-equivalent tool exists, else API fallback | Preferred for `paperclip-monitor`. |
| Activity log | CLI `paperclipai activity list --json` | `paperclipApiRequest`, then direct REST | Use CLI for ordinary monitoring. |
| Costs | CLI/dashboard if exposed | `paperclipApiRequest`, then direct REST | Use API fallback for detailed cost drill-down if summaries are insufficient. |
| Company skill library | CLI `paperclipai skills ...` | direct REST if documented | MCP currently lacks skill-library tools. |
| Local CLI setup/auth/context | CLI | none | Use `paperclipai` for local environment work. |
| Read llm-wiki page content | `paperclip-wiki-fetch` with MCP `paperclipApiRequest` | direct REST `POST /api/plugins/paperclipai.plugin-llm-wiki/data/page-content` | No documented CLI wiki command and no `/api/wiki/...` route. Extract page path from SPA URLs. |
| List llm-wiki pages | `paperclip-wiki-fetch` with MCP `paperclipApiRequest` | direct REST `POST /api/plugins/paperclipai.plugin-llm-wiki/data/pages` | Include `companyId`, `wikiId`, and `spaceSlug` in `params`. |
| List llm-wiki captured sources | `paperclip-wiki-fetch` with MCP `paperclipApiRequest` | direct REST `POST /api/plugins/paperclipai.plugin-llm-wiki/data/sources` | Use before choosing among captured raw sources. |
| Create or update llm-wiki page | `paperclip-wiki-manage` via `POST /api/plugins/paperclipai.plugin-llm-wiki/actions/write-page` | direct REST with board bearer auth | Must read current state, show exact JSON and markdown diff/body, get approval, write, then read back. Use `expectedHash` for existing pages. |
| Rename, move, archive, or delete llm-wiki page/source | `paperclip-wiki-manage` with a confirmed plugin bridge write route | `paperclipApiRequest`, then direct REST after route/schema confirmation | Destructive or path-changing operations require explicit target/action approval and readback verification. |

## Verified REST Shapes

Use these only after the CLI and MCP API request surfaces are unavailable or broken. Prefer company-scoped create/list routes and direct record update routes where verified.

| Entity | Operation | Verified REST shape | Notes |
|---|---|---|---|
| Goals | List | `GET /api/companies/{companyId}/goals` | Use to confirm existing goal tree before writes. |
| Goals | Create | `POST /api/companies/{companyId}/goals` | Include native `level`, `status`, `parentId` when relevant, and `ownerAgentId` only for agent-owned goals. |
| Goals | Update | `PATCH /api/goals/{goalId}` | Verified for reparenting. `PATCH /api/companies/{companyId}/goals/{goalId}` may return route not found. |
| Projects | List | `GET /api/companies/{companyId}/projects` | Use to confirm existing durable channel or motion projects. |
| Projects | Create | `POST /api/companies/{companyId}/projects` | Link goals with `goalIds` when creating or updating, then verify `goalIds` or expanded goals in readback. |
| Projects | Update | `PATCH /api/projects/{projectId}` | Use native `goalIds` or equivalent field. |

## Skill Guidance

**paperclip-setup**

- Use CLI for local `paperclipai` path, version, context, and company list.
- Configure and verify MCP only after CLI context/auth are usable.
- Use bundled templates for project docs.

**paperclip-clarify**

- Usually no Paperclip mutation.
- Use CLI/MCP reads only when an answer can be discovered from current Paperclip state.

**paperclip-record-strategy**

- Use CLI first for reads/writes that it supports and verifies.
- Use native CLI goal/project CRUD and issue document commands when available.
- Use MCP or `paperclipApiRequest` only when the installed CLI lacks the required native field or verification.
- Fall back to embedding the plan in the issue description only when CLI, MCP, and API access are unavailable or explicitly rejected.
- Use `paperclip-wiki-fetch` before drafting plan documents when approved inputs reference wiki URLs, page paths, or captured sources.
- Use `paperclip-wiki-manage` only when the operator explicitly asks to publish or sync a strategy artifact to wiki; Paperclip plan documents remain the default source of truth.

**paperclip-plan-work**

- Use CLI issue reads/writes first when they support the needed fields and JSON verification.
- Use MCP issue tools when CLI lacks a native field or would require brittle parsing.
- Create and verify one child issue at a time before continuing.
- Create planned issues as `backlog` and unassigned only.
- Do not move issues to `todo`, assign, checkout, or manually invoke heartbeats from planning.
- Verify `parentId`, `projectId`, `goalId`, `status`, null assignee, and `blockedByIssueIds` after each write.
- Use MCP document tools for plan-document reads/writes when CLI lacks native document commands.
- Use `paperclipApiRequest` for fields not exposed by CLI/MCP, including blocker links.
- Use `paperclip-wiki-fetch` when parent plans, comments, or issue bodies reference wiki source material needed for child issue detail.
- Use `paperclip-wiki-manage` only when the operator explicitly asks to publish, sync, or update wiki content from planning output.
- Stop on the first unrepaired structural mismatch and report partial state.

**paperclip-triage**

- Use CLI issue reads/updates/comments first when they support the needed fields and verification.
- Use MCP issue tools when CLI cannot perform or verify the mutation.
- Use `paperclipApiRequest` only for fields not exposed by CLI/MCP.
- Recommend first, mutate after approval.
- Triage is the phase that may recommend moving ready backlog issues to `todo`.
- Use agent participants in `executionPolicy.stages[]` for recommended issue reviewer gates, and verify the field after mutation. Represent required human final acceptance in the handoff as an agent-owned `request_confirmation`, not a user approval stage.
- Use `paperclip-wiki-fetch` when readiness depends on referenced wiki source material.
- Recommend `paperclip-wiki-manage` for wiki content corrections, but do not mutate wiki pages from ordinary triage unless the operator explicitly switches to wiki management.

**paperclip-monitor**

- Use CLI dashboard, activity, approvals, agents, and issues first.
- Use `paperclipai issue live-runs`, `active-run`, `runs`, and `recovery-actions` for execution drill-down.
- Use MCP or `paperclipApiRequest` for deeper drill-down when CLI summaries are insufficient.
- Treat `wake queued`, queued/running runs, and `workspace ready` as healthy pickup states. Observe read-only; do not recommend duplicate dispatch or mutation merely because execution has not finished.

**paperclip-admin**

- Use CLI for reads and writes when it supports the needed operation and verification.
- Use MCP for reads/writes not exposed cleanly through CLI.
- Use `paperclipApiRequest` or direct REST for small record repairs not exposed through CLI/MCP.
- Ask before any mutation, especially attaching skills, changing budgets, changing runtimes, or making work startable.
- For reviewer assignment changes, patch and verify issue `executionPolicy.stages[].participants`; do not use `reviewRequest` as the reviewer source of truth.
- Executors submit to execution policy by transitioning to `done`; verify the runtime-created `in_review` state and agent `executionState.currentParticipant` instead of manually routing review.
- For ordinary human final acceptance, require the agent reviewer to create and wait on `request_confirmation`. Do not configure the operator as a user approval-stage participant; verify the pending interaction, then its accepted/rejected status and resume result.
- For delegation, preserve the executor's default environment, complete and verify the handoff/reviewer gate while unassigned, confirm no live runs or unresolved recovery actions, then assign exactly once. Do not pair assignment with heartbeat/resume, mentions, checkout, comments, or another assignment wake.
- After dispatch is queued/running, remain read-only. For correction, interrupt/cancel once and wait for live runs, process recovery, comment retries, and relevant recovery actions to settle before unassigning, repairing, or reassigning.
- Verify every changed record after the write.
- Route wiki content mutations to `paperclip-wiki-manage` instead of treating them as generic admin edits.

**paperclip-create-agent**

- Use CLI reads for context where available, MCP reads when CLI lacks detail, then `paperclipApiRequest` or direct REST for native agent creation or hire submission.
- Prefer `/agent-hires` when governance is required or board visibility is useful; use direct `/agents` only with explicit operator approval.
- Mirror company conventions from existing agents, org chart, skills, adapter configuration docs, and current agent configuration examples.
- Create managed instructions bundles for local agents instead of durable legacy prompt fields.
- Leave timer heartbeats disabled by default; enable scheduled heartbeats only with explicit justification.
- After creation, verify agent fields and approval state before creating keys, syncing skills, or assigning work. Do not manually invoke another agent's heartbeat; Paperclip agents wake through their own heartbeat policy after eligible assignment.
