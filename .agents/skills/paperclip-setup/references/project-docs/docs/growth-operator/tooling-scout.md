# Growth Tooling Scout

Growth Tooling Scout is a reusable research and decision loop for acquisition tools. It prevents the Growth Operator suite from hard-coding vendor assumptions before a tool has been evaluated against a real growth need.

## When To Run

Run this before:

- adopting a new inbound, outbound, enrichment, sequencing, CRM, analytics, or automation tool
- adding tool-specific instructions to `outbound-triage`, `inbound-triage`, or planning skills
- creating a tool-specific skill such as an Instantly, Clay, or Grinfi skill
- building custom glue, scripts, MCP tools, browser workflows, or Paperclip plugins for growth operations

Do not run this for a tool if the operator has already made a narrow administrative decision and only needs a small approved setup change.

## Decision Ladder

Prefer the highest rung that satisfies the current growth need:

1. `Adopt` - use the tool directly.
2. `Integrate` - wire the tool into the current stack through exports, APIs, webhooks, n8n, Paperclip, or existing connectors.
3. `Extend` - build a small wrapper, skill, plugin, or script on top of the tool.
4. `Build` - build custom tooling only when the need is proven and adopt/integrate/extend all fail.
5. `Defer` - do not act because the need is speculative, risky, or not tied to current growth work.

## Fit Rubric

Score each candidate from 0 to 5. Weighted maximum is 100.

| Criterion | Weight | What Good Looks Like |
| --- | ---: | --- |
| Fit to current growth need | 3 | Solves the exact active inbound/outbound job. |
| Revenue or validation leverage | 3 | Helps book calls, learn from the market, build trust, or validate a wedge now. |
| Reuse leverage | 3 | Avoids building something mature tools already handle. |
| Data control and portability | 2 | Inputs, outputs, logs, and learnings can be exported or mirrored. |
| Account-action safety | 2 | Supports clear approval gates, caps, suppressions, audit, and rollback. |
| Cost and credit control | 2 | Costs, credits, enrichment usage, and send volume can be bounded. |
| Compliance and consent fit | 2 | Supports compliant contact handling and suppression workflows. |
| Stack fit | 1 | Fits Paperclip, n8n, files/sheets, current outbound tools, and human review. |
| Operational burden | 1 | Easy enough to run without becoming a new platform project. |
| Replaceability | 1 | Can be swapped without losing the durable acquisition ledger. |

Use these thresholds:

- `>= 70` - strong candidate.
- `50-69` - viable with caveats or a timeboxed trial.
- `< 50` - reject for this need.

## Required Checks

For every evaluated tool, check:

- official docs and pricing or plan limits
- export and API surfaces
- contact-data handling, suppression, and compliance controls
- sender-account, CRM, or external-account permissions
- credit/budget controls
- security, secrets, telemetry, and data-retention posture
- whether our durable data can live outside the tool
- what must remain human-approved

## Output

Use this shape:

```markdown
## Need

## Current Growth Context

## Candidates

| Tool | Role | Evidence | Weighted Score | Decision |
| --- | --- | --- | ---: | --- |

## Security, Compliance, And Account-Action Notes

## Recommendation

## Smallest Next Action

## Approval Needed

## Defer / Build-Trap Check
```

## Mutation Rule

Growth Tooling Scout is non-mutating. Do not create accounts, change settings, spend credits, launch campaigns, create Paperclip records, or attach tools without explicit operator approval through the relevant admin or planning skill.
