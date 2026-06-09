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
- no company skill-library tools
- no secret, plugin, cloud, routine, or worktree tools
- no dedicated project create/update tools in the published MCP list; use `paperclipApiRequest` if CLI cannot do the native operation

Treat write schemas as claims to verify, not proof. After every write, read the record back and confirm parent, project, goal, status, assignee, document, approval, and blocker fields before continuing with dependent mutations.

## Operation Matrix

| Operation | Preferred surface | Fallback | Notes |
|---|---|---|---|
| Check active Paperclip company | CLI `paperclipai context show --json` | MCP `paperclipMe` / `paperclipListAgents` | MCP tools use explicit env or active CLI context. CLI remains the setup authority. |
| Derive API auth | CLI auth store | `PAPERCLIP_API_KEY` env var | Use `paperclipai auth whoami --json` to verify board auth. Stored board credentials live in `~/.paperclip/auth.json`; do not print tokens. |
| List companies | CLI `paperclipai company list --json` | direct REST | No dedicated MCP company list tool. |
| Export/import company | CLI `paperclipai company export/import` | direct REST if documented | Use CLI for backup/restore workflows. |
| List goals | CLI if available with JSON | MCP `paperclipListGoals` | Verify response shape before using goal ids in mutations. |
| Get goal | CLI if available with JSON | MCP `paperclipGetGoal` | Use MCP when CLI lacks the read. |
| Create/update goal | CLI if available and verifies native fields | `paperclipApiRequest`, then direct REST | No dedicated goal write tool in MCP 0.1.0. Must support `level`, `status`, `parentId`, and `ownerAgentId`; verify the record. |
| List projects | CLI if available with JSON | MCP `paperclipListProjects` | Use MCP when CLI lacks project reads. |
| Get project | CLI if available with JSON | MCP `paperclipGetProject` | Use MCP when CLI lacks project detail. |
| Create project | CLI if available and verifies native fields | `paperclipApiRequest`, then direct REST | Required for missing planning-chain projects. |
| Update project / link goals | CLI if available and verifies native fields | `paperclipApiRequest`, then direct REST | Use native `goalIds` or equivalent field. |
| List issues | CLI `paperclipai issue list --json` | MCP `paperclipListIssues` | MCP supports richer filters; use it when CLI output is insufficient. |
| Get issue detail | CLI `paperclipai issue get --json` | MCP `paperclipGetIssue` | Use before triage or planning. |
| Create parent issue | CLI `paperclipai issue create` if fields verify | MCP `paperclipCreateIssue` | Include project/parent/status fields when known and verify after creation. |
| Create child issue | CLI if parent linkage verifies | MCP `paperclipCreateIssue`, then `paperclipApiRequest` repair | Create one issue, verify `parentId`, repair if possible, then continue. |
| Update issue lifecycle/fields | CLI `paperclipai issue update` if fields verify | MCP `paperclipUpdateIssue` | Planning leaves issues in `backlog`. Only triage/delegation may move work to `todo` after approval. |
| Write blocker links | CLI if `blockedByIssueIds` verifies | MCP `paperclipUpdateIssue`, then `paperclipApiRequest` | Do not replace first-class blockers with comments unless the operator approves degraded mode. |
| Comment on issue | CLI `paperclipai issue comment` | MCP `paperclipAddComment` | Use comments for triage reasoning. |
| Checkout/release issue | CLI `paperclipai issue checkout/release` | MCP `paperclipCheckoutIssue` / `paperclipReleaseIssue` | Respect checkout conflict semantics. |
| Delete issue | direct REST only after explicit approval | none | The current CLI/MCP inspected surfaces do not expose issue delete as a normal operator command. |
| Read/write `plan` document | CLI if available and verifies document record | MCP `paperclipGetDocument` / `paperclipUpsertIssueDocument` | Prefer keyed issue documents over issue-description fallback. |
| List approvals | CLI `paperclipai approval list --json` | MCP `paperclipListApprovals` / `paperclipListIssueApprovals` | Monitoring and board-decision workflows. |
| Resolve approvals | CLI `paperclipai approval approve/reject/request-revision/resubmit` | MCP `paperclipApprovalDecision` | Verify approval status after mutation. |
| List agents | CLI `paperclipai agent list --json` | MCP `paperclipListAgents` | Use CLI for local agent setup commands. |
| Create agents / hire agents | CLI if available and governance path verifies | `paperclipApiRequest`, then direct REST | Use `paperclip-create-agent`. Inspect org/config/skills first, ask approval, create or submit hire, then verify agent and approval state. |
| Update existing agents | CLI depending operation | MCP reads, then `paperclipApiRequest` or direct REST | Use `paperclip-admin`. Inspect current agent and skills first, ask approval, then verify the updated agent. |
| Dashboard summary | CLI `paperclipai dashboard get --json` | MCP if a dedicated/dashboard-equivalent tool exists, else API fallback | Preferred for `paperclip-monitor`. |
| Activity log | CLI `paperclipai activity list --json` | `paperclipApiRequest`, then direct REST | Use CLI for ordinary monitoring. |
| Costs | CLI/dashboard if exposed | `paperclipApiRequest`, then direct REST | Use API fallback for detailed cost drill-down if summaries are insufficient. |
| Company skill library | CLI `paperclipai skills ...` | direct REST if documented | MCP currently lacks skill-library tools. |
| Local CLI setup/auth/context | CLI | none | Use `paperclipai` for local environment work. |

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
- Use MCP for project reads and plan documents when CLI lacks a native operation.
- Use `paperclipApiRequest` for project create/update or goal create/update when no CLI or dedicated MCP tool supports the required native fields.
- Fall back to embedding the plan in the issue description only when CLI, MCP, and API access are unavailable or explicitly rejected.

**paperclip-plan-work**

- Use CLI issue reads/writes first when they support the needed fields and JSON verification.
- Use MCP issue tools when CLI lacks a native field or would require brittle parsing.
- Create and verify one child issue at a time before continuing.
- Create planned issues as `backlog` and unassigned only.
- Do not move issues to `todo`, assign, checkout, or manually invoke heartbeats from planning.
- Verify `parentId`, `projectId`, `goalId`, `status`, null assignee, and `blockedByIssueIds` after each write.
- Use MCP document tools for plan-document reads/writes when CLI lacks native document commands.
- Use `paperclipApiRequest` for fields not exposed by CLI/MCP, including blocker links.
- Stop on the first unrepaired structural mismatch and report partial state.

**paperclip-triage**

- Use CLI issue reads/updates/comments first when they support the needed fields and verification.
- Use MCP issue tools when CLI cannot perform or verify the mutation.
- Use `paperclipApiRequest` only for fields not exposed by CLI/MCP.
- Recommend first, mutate after approval.
- Triage is the phase that may recommend moving ready backlog issues to `todo`.

**paperclip-monitor**

- Use CLI dashboard, activity, approvals, agents, and issues first.
- Use MCP or `paperclipApiRequest` for deeper drill-down when CLI summaries are insufficient.

**paperclip-admin**

- Use CLI for reads and writes when it supports the needed operation and verification.
- Use MCP for reads/writes not exposed cleanly through CLI.
- Use `paperclipApiRequest` or direct REST for small record repairs not exposed through CLI/MCP.
- Ask before any mutation, especially attaching skills, changing budgets, changing runtimes, or making work startable.
- Verify every changed record after the write.

**paperclip-create-agent**

- Use CLI reads for context where available, MCP reads when CLI lacks detail, then `paperclipApiRequest` or direct REST for native agent creation or hire submission.
- Prefer `/agent-hires` when governance is required or board visibility is useful; use direct `/agents` only with explicit operator approval.
- Mirror company conventions from existing agents, org chart, skills, adapter configuration docs, and current agent configuration examples.
- Create managed instructions bundles for local agents instead of durable legacy prompt fields.
- Leave timer heartbeats disabled by default; enable scheduled heartbeats only with explicit justification.
- After creation, verify agent fields and approval state before creating keys, syncing skills, or assigning work. Do not manually invoke another agent's heartbeat; Paperclip agents wake through their own heartbeat policy after eligible assignment.
