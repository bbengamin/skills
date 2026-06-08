---
name: creator-record-strategy
description: Materialize an approved Creator Growth clarification summary into Paperclip goals, a creator project, strategy parent issues, campaign parent issues, and plan documents one missing layer at a time. Use after creator-clarify when the operator approves recording or revising creator-led distribution strategy.
---

# Creator Record Strategy

Record approved creator-growth intent into Paperclip. Create or update only the next missing layer unless the operator approves a larger proposal.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/creator-operator/workflow.md`
- `../../../docs/creator-operator/control-plane.md`
- `../../../docs/paperclip-operator/cli-contract.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

## Process

1. Confirm there is an approved Creator Clarification Summary or equivalent operator-approved strategy.
2. Inspect current Paperclip goals, projects, candidate parent issues, plan documents, and related comments.
3. Decide which layer is missing or being revised:
   - durable creator-growth goal
   - related creator/persona goal
   - related expertise goal
   - creator project
   - yearly strategy parent issue
   - quarterly strategy parent issue
   - monthly strategy parent issue
   - channel/campaign parent issue
   - plan document on an existing parent issue
4. Draft the exact proposed mutation.
5. Ask for approval before mutating Paperclip.
6. Apply only approved changes.
7. Read back the created or updated records and report identifiers.

## Entity Guidance

Use goals for stable direction:

- `Build creator-led distribution as a repeatable acquisition asset`
- `Use <creator>'s founder brand to generate trust and qualified conversations`
- `Establish <creator>'s <domain> expertise`

Use one project per creator/persona:

- `Creator ops: <creator>`

Use parent issues and plan documents for time and campaign structure:

```text
Creator strategy 2026
└── Creator strategy Q3 2026
    └── Creator strategy June 2026
        └── LinkedIn campaign: logistics hypothesis X
```

Do not create new goals for every month, channel, or short-lived campaign unless the operator explicitly wants that.

## Strategy Plan Document

Recommended plan shape:

```markdown
## Outcome

## Creator/Persona

## Time Horizon

## Channels

## Audience/ICP

## Hypothesis

## Positioning And Story

## Source Material

## Scope

## Non-Goals

## Success Signals

## Constraints

## Risks

## Validation

## Stop Conditions

## Planning Notes
```

When revising an existing period plan, update the existing plan document after approval and add a comment summarizing why it changed. Create a new issue only for a distinct strategy object, campaign, or executable work item.

## Surface Rules

Use the narrowest Paperclip surface that supports the native field. Read `integration-matrix.md` before choosing MCP, CLI, or REST.

Run a REST auth preflight before the first REST mutation. Never print bearer tokens. If a native field cannot be written, stop and ask the operator instead of silently degrading the strategy artifact.

## Mutation Rule

Always present the exact proposed goals, project, issues, plan body, comments, and status changes before creating or updating Paperclip.
