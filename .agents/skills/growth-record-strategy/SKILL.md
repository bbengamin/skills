---
name: growth-record-strategy
description: Materialize an approved Growth Clarification Summary into Paperclip goals, durable channel/motion projects, strategy parent issues, branch parent issues, campaign parent issues, and plan documents one missing layer at a time. Use after growth-clarify when the operator approves recording or revising acquisition strategy.
---

# Growth Record Strategy

Record approved growth strategy into Paperclip. Create or update only the next missing layer unless the operator approves a larger proposal.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/growth-operator/workflow.md`
- `../../../docs/growth-operator/control-plane.md`
- `../../../docs/paperclip-operator/cli-contract.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

## Process

1. Confirm there is an approved Growth Clarification Summary or equivalent operator-approved strategy.
2. Inspect current Paperclip goals, projects, candidate parent issues, plan documents, and related comments.
3. Decide which layer is missing or being revised:
   - durable acquisition company goal
   - inbound or outbound team goal
   - expertise, vertical, channel, or motion team goal
   - durable channel or motion project
   - yearly strategy parent issue
   - quarterly strategy parent issue
   - monthly strategy parent issue
   - inbound branch parent issue
   - outbound branch parent issue
   - campaign or experiment parent issue
   - plan document on an existing parent issue
4. Draft the exact proposed mutation.
5. Ask for approval before mutating Paperclip.
6. Apply only approved changes.
7. Read back created or updated records and report identifiers.

## Entity Guidance

Use goals for stable acquisition direction. Every proposed goal mutation must specify `title`, `level`, `status`, `parentId` when it is a child goal, and `ownerAgentId` only for real agent-owned goals.

```text
[company] Build repeatable acquisition
|-- [team] Build inbound trust engine through <creator>'s personal brand
|   `-- [team] Establish <creator>'s <domain> expertise brand
`-- [team] Build outbound engine for operator walkthroughs and validation
    `-- [team] Build repeatable <vertical/persona> outreach motion
```

Default goal mapping:

- `company` for the root acquisition north star, for example `Build repeatable acquisition`.
- `team` for durable inbound, outbound, creator, expertise, vertical, channel, validation, or motion outcomes.
- `agent` only when assigning ownership to a specific Paperclip agent; set `ownerAgentId`.
- `task` rarely; prefer parent issues or child issues for campaigns, months, lead lists, sequences, content sprints, and executable work.

Use projects for durable channels or motions:

- `Inbound: Ihor LinkedIn`
- `Inbound: Ihor Newsletter`
- `Outbound: Operator walkthroughs`
- `Outbound: Partnerships and warm intros`

Use parent issues and plan documents for strategy periods, branches, campaigns, and experiments:

```text
Growth 2026
`-- Growth strategy Q3 2026
    `-- June inbound logistics strategy
        `-- LinkedIn campaign: logistics workflow pain
```

```text
Outbound growth 2026
`-- Outbound strategy Q3 2026
    `-- June construction walkthrough strategy
        `-- Campaign: estimate-to-invoice walkthroughs
```

Do not create new goals for every month, short-lived campaign, message sequence, lead list, content sprint, or learning artifact.

## Strategy Plan Document

Recommended plan shape:

```markdown
## Outcome

## Goal Structure

## Projects

## Time Horizon

## Market / Vertical

## ICP / Buyer / Persona

## Wedge Or Painful Workflow

## Inbound Role

## Outbound Role

## Shared Proof And Source Material

## Artifact Ask

## Offer / CTA

## Scope

## Non-Goals

## Success Signals

## Constraints

## Risks

## Validation

## Stop Conditions

## Branch Planning Notes
```

When revising an existing strategy plan, update the existing plan document after approval and add a comment summarizing why it changed. Create a new issue only for a distinct strategy object, branch, campaign, experiment, or executable work item.

## Surface Rules

Use the CLI-first ladder in `integration-matrix.md`: CLI when it supports and verifies the native field, dedicated MCP tools when CLI is insufficient, `paperclipApiRequest` when no dedicated tool exists, and direct REST only when CLI and MCP are unavailable or broken.

Before the first MCP API request or direct REST mutation, derive API base and company from `paperclipai context show --json`, verify auth with `paperclipai auth whoami --json`, and never print bearer tokens. If a native field cannot be written, stop and ask the operator instead of silently degrading the strategy artifact.

## Mutation Rule

Always present the exact proposed goals, including `level`, `status`, `parentId`, and `ownerAgentId`, plus projects, issues, plan body, comments, and status changes before creating or updating Paperclip.
