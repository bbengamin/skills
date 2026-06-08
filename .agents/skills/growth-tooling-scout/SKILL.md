---
name: growth-tooling-scout
description: Evaluate acquisition tools before adoption, integration, extension, or custom build. Use when considering inbound, outbound, enrichment, sequencing, CRM, analytics, automation, Instantly, Clay, Grinfi, n8n, Paperclip plugin, MCP, or custom growth tooling decisions.
---

# Growth Tooling Scout

Run a non-mutating tool evaluation for growth operations.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/growth-operator/tooling-scout.md`
- `../../../docs/growth-operator/control-plane.md`

Open when Paperclip lifecycle or mutation rules matter:

- `../../../docs/paperclip-operator/control-plane.md`
- `../../../docs/paperclip-operator/integration-matrix.md`

## Process

1. Define the need in one sentence: what job the tool must do and which active growth work it accelerates.
2. If the need is not tied to current acquisition, validation, inbound, outbound, or operator workflow learning, recommend `Defer`.
3. Inspect existing repo docs, Paperclip context, and prior strategy artifacts when they can answer context questions.
4. Research official docs, pricing/limits, API/export surfaces, security/compliance notes, and credible alternatives.
5. Shortlist 3-6 candidates when the operator is choosing among tools. If the operator named one tool, evaluate that tool plus at least one fallback when practical.
6. Score candidates using `docs/growth-operator/tooling-scout.md`.
7. Classify each candidate: `Adopt`, `Integrate`, `Extend`, `Build`, or `Defer`.
8. Identify approval gates and what must remain human-controlled.
9. Output a recommendation and smallest next action.

## Tooling Roles

Classify the tool's role before scoring:

- lead sourcing
- enrichment
- personalization
- sequencing
- deliverability
- CRM or pipeline
- reply handling
- analytics
- automation/glue
- Paperclip/plugin/MCP integration
- data ledger or export layer

## Output

Use this shape:

```markdown
## Growth Tooling Scout Result

### Need

### Current Growth Context

### Tooling Role

### Candidates

| Tool | Role | Evidence | Weighted Score | Decision |
| --- | --- | --- | ---: | --- |

### Security, Compliance, And Account-Action Notes

### Recommendation

### Smallest Next Action

### Approval Needed

### Defer / Build-Trap Check
```

## Stop Conditions

Stop and ask the operator when:

- the tool would require real accounts, credentials, paid credits, sender accounts, CRM mutation, or contact upload before evaluation is complete
- official docs or pricing are unavailable for a material decision
- the need is too vague to score
- the tool would become the source of truth for durable growth data without an export or mirroring plan
- the recommendation is `Build` and adopt/integrate/extend alternatives have not been evaluated

## Mutation Rule

Never create accounts, change settings, spend credits, launch campaigns, upload contacts, create Paperclip records, or attach tools from this skill. Recommend first; use the relevant admin or planning skill after explicit approval.
