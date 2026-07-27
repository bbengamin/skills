# Paperclip Docs Index

These upstream sources inform the Paperclip operator suite. Last audited 2026-07-27 against stable `paperclipai` `2026.722.0` and the `paperclipai/paperclip` `v2026.722.0` tag. Canary releases are useful for spotting upcoming drift but must not become the operator contract until stable or verified in the target environment.

## Start And Architecture

- Docs home: https://docs.paperclip.ing/#/
- Core concepts: https://docs.paperclip.ing/#/start/core-concepts
- Architecture: https://docs.paperclip.ing/#/start/architecture
- Source repository: https://github.com/paperclipai/paperclip

## Board Operator Guides

- Delegation: https://docs.paperclip.ing/#/guides/board-operator/delegation
- Managing tasks: https://docs.paperclip.ing/#/guides/board-operator/managing-tasks
- Managing agents: https://docs.paperclip.ing/#/guides/board-operator/managing-agents
- Execution workspaces and runtime services: https://docs.paperclip.ing/#/guides/board-operator/execution-workspaces-and-runtime-services
- Approvals: https://docs.paperclip.ing/#/guides/board-operator/approvals
- Activity log: https://docs.paperclip.ing/#/guides/board-operator/activity-log
- Dashboard: https://docs.paperclip.ing/#/guides/board-operator/dashboard
- Costs and budgets: https://docs.paperclip.ing/#/guides/board-operator/costs-and-budgets

## Agent Execution Guides

- Heartbeat protocol: https://docs.paperclip.ing/#/guides/agent-developer/heartbeat-protocol
- Task workflow: https://docs.paperclip.ing/#/guides/agent-developer/task-workflow
- Comments and communication: https://docs.paperclip.ing/#/guides/agent-developer/comments-and-communication
- Handling approvals and confirmations: https://docs.paperclip.ing/#/guides/agent-developer/handling-approvals
- Execution policy: https://docs.paperclip.ing/#/guides/execution-policy
- Writing a skill: https://docs.paperclip.ing/#/guides/agent-developer/writing-a-skill
- Skills store: https://docs.paperclip.ing/#/guides/agent-developer/skills-store

## CLI And API

- CLI overview: https://docs.paperclip.ing/#/cli/overview
- Control-plane commands: https://docs.paperclip.ing/#/cli/control-plane-commands
- Setup commands: https://docs.paperclip.ing/#/cli/setup-commands
- API overview: https://docs.paperclip.ing/#/api/overview
- Issues API: https://docs.paperclip.ing/#/api/issues
- Agents API: https://docs.paperclip.ing/#/api/agents
- Goals and projects API: https://docs.paperclip.ing/#/api/goals-and-projects
- Approvals API: https://docs.paperclip.ing/#/api/approvals
- Activity API: https://docs.paperclip.ing/#/api/activity
- Dashboard API: https://docs.paperclip.ing/#/api/dashboard

## Audit Method

When refreshing this suite:

1. Record the current stable npm version and target environment CLI version.
2. Compare upstream commits and relevant docs since the previous audit date/tag.
3. Inspect `paperclipai <resource> --help` rather than assuming CLI coverage from old docs.
4. Verify behavior-changing semantics against stable source/docs, especially assignment wakes, execution policy, interactions, run recovery, and field names.
5. Update canonical docs first, then synchronize bundled skill references and validate every `SKILL.md` frontmatter block.
