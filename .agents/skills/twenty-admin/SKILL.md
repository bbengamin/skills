---
name: twenty-admin
description: Twenty CRM operator skill for Right.Link. Use when the user wants to inspect or mutate Twenty CRM records, run identity-based match-or-create, audit Twenty schema/metadata, draft a Twenty execution company skill, or map Paperclip outbound-engine issues to safe CRM operations. Reads freely; dry-runs before writes; asks before every Twenty or Paperclip mutation.
---

# Twenty Admin

Operate Twenty CRM, the Right.Link sales system of record, through the approved MCP. Keep every run predictable: connect, learn exact tool schemas, inspect current state, dry-run any intended write, ask for approval, execute only the approved change, then read back.

Twenty is shared with live sales work. Default to additive, non-destructive changes. Never send outreach, spend enrichment credits, delete records, or modify owner-specific structures unless the operator explicitly approves that exact action.

## Branches

Use this skill for:

- Twenty reads: look up people, companies, campaigns, opportunities, notes, tasks, or metadata.
- Twenty writes: create, update, or match-or-create CRM records after an approved dry-run.
- Schema audits: inspect object/field metadata and identify safe additive extensions.
- Execution-skill drafting: draft or revise Paperclip company skills that teach engine agents how to use Twenty safely, such as RL-438.

Route elsewhere when:

- The request mutates Paperclip issues, agents, company skills, assignments, or approvals: use `paperclip-admin`.
- The request creates or installs a Paperclip company skill in the library: use `paperclip-admin` after this skill drafts the content.
- The request plans or triages outbound work: use `outbound-plan-work`, `outbound-triage`, or the shared growth skills.
- The request sends outreach, launches sequences, enriches/spends credits, or changes external channel tools: use the dedicated channel skill or tool flow.

## Operating Loop

1. Confirm connectivity with `mcp__metamcp__twenty__list_object_metadata_names`.
   Done when the object list returns or the failure is reported with the current MCP config state.
2. Load exact operation schemas from the catalog.
   Done when every operation you intend to call has been learned with `learn_tools`.
3. Inspect current state before changing anything.
   Done when the target records, identity keys, relevant metadata, and guarded fields are known or explicitly unavailable.
4. For read-only work, answer with records, record ids, uncertainty, and source operation names.
   Done when the user can tell what was read and what remains unknown.
5. For mutating work, produce a dry-run.
   Done when each target record is classified as `would-create`, `would-update`, `collision-skip`, or `blocked`, with field-level diffs.
6. Ask for approval before any create, update, upsert, metadata change, action, delete, Paperclip mutation, or external-account effect.
   Done only when the operator approves the exact action.
7. Execute only the approved operation.
   Done when no extra records, fields, tools, or side effects are included.
8. Read back and verify.
   Done when every changed record is fetched again and the expected fields, ids, and guarded non-changes are confirmed.

## Twenty MCP

Twenty is exposed through the `metamcp` aggregator under the `twenty` namespace. Tools are named `mcp__metamcp__twenty__*`.

The MCP server is `metamcp` in `.mcp.json`, using native SSE:

```json
"metamcp": {
  "type": "sse",
  "url": "https://metamcp.dev.right.link/metamcp/sales/sse",
  "headers": { "Authorization": "Bearer <token>" }
}
```

If Twenty tools are missing:

1. Run `claude mcp list` and confirm `metamcp` is connected.
2. If it failed, verify the entry is native SSE with a Bearer header.
3. Do not configure it through `mcp-proxy`; that package is a stdio-to-SSE server wrapper and treats the URL as a command.
4. After config changes, restart Claude Code or start a new session before expecting tools to appear.

## Tool Pattern

Use the meta-tool layer. Do not guess concrete operation schemas.

1. `mcp__metamcp__twenty__list_object_metadata_names` for connectivity and object names.
2. `mcp__metamcp__twenty__get_tool_catalog` to browse available operations by category.
3. `mcp__metamcp__twenty__learn_tools` to fetch exact input schemas for every intended operation in one call.
4. `mcp__metamcp__twenty__execute_tool` to run an operation by exact learned name and schema.

Load Twenty built-in playbooks through `list_skills` / `load_skills` when the catalog shows a matching playbook, especially `data-manipulation` or `metadata-building`.

## Core Model

Workspace objects include the standard Twenty set (`people`, `companies`, `opportunities`, `notes`, `tasks`, …) plus the outbound-engine golden-record objects built on top of it: `campaign` (reused as the engine campaign), `campaignMembership` (the suppression authority joining person ↔ campaign), `campaignTouch` (per-event touch history), `sendingAccount`, and `engineConfig`.

Person identity precedence:

1. `linkedinLink.primaryLinkUrl`
2. `emails.primaryEmail`

Two Person records are the same person if either key matches. Person also has `companyId`, plus the engine fields `activeCampaignMembershipId` (the one-active-campaign-per-person pointer) and a `campaignMemberships` collection.

The engine golden-record schema (identity keys, resolution, dedup/merge, suppression, routing) is documented in the `twenty-engine-sync` execution skill. This operator skill owns schema/metadata work and audits; it defers record-level engine read/write to that skill.

Before non-trivial writes, run a fresh `get_object_metadata` / `get_field_metadata` audit. Treat fields or relations with unclear ownership, existing workflow semantics, or populated values as guarded until the operator confirms they are safe to modify.

When adding custom objects/fields: `type` is a reserved field name (use a qualified name like `touchType`); new custom fields/objects are filed under the existing custom application id — there is no operator-settable application namespace on the metadata create path; and `create_many_field_metadata` validates atomically, so one invalid field rejects the whole batch.

## Query Rules

- `select` is required on `find_*`; use `"*"` or an explicit field list.
- MANY_TO_ONE relations are read through the foreign key column, for example `companyId`.
- Filter fields are top-level keys with operator objects, for example `{ "emails": { "primaryEmail": { "eq": "a@b.com" } } }`.
- Do not wrap filters in a `filter` object.
- Do not put bare `eq`, `ilike`, or similar operators at the top level.
- Use `and`, `or`, and `not` arrays for compound filters.
- `orderBy` uses scalar or composite objects, not dot notation.

## Idempotent Match-Or-Create

For each input record:

1. Query by all available identity keys with `find_many_<object>` and explicit `select`.
2. If zero matches, classify as `would-create`.
3. If one match, classify as `would-update` by id, additive only.
4. If more than one match, classify as `collision-skip` and do not write.

Use `upsert_many_<object>` only after confirming the match field has a backing unique constraint. Standard email and LinkedIn fields are not unique by default.

## Mutations

Read freely. Ask before any create, update, upsert, delete, schema change, action, Paperclip mutation, outreach, enrichment, or credit-spending operation.

Especially explicit approval is required for:

- any `delete_*`
- overwriting a populated field
- shrinking or removing values from a multi-value field
- writes onto or near guarded objects or fields
- any METADATA/schema change
- any ACTION that contacts a person, drafts email, sends email, navigates an external app, or spends credits
- creating, updating, installing, or attaching a Paperclip company skill

When identity is ambiguous, stop. Report the collision and ask the operator how to resolve it.

## Execution-Skill Drafting

The outbound golden-record execution skill `twenty-engine-sync` is already drafted and installed in the company skill library — it covers query, identity resolution, idempotent match-or-create, additive writes, golden-record merge/survivorship, fuzzy->QA routing, suppression, and routing. Revise it rather than re-drafting; create a new execution skill only for a genuinely separate capability.

When drafting or revising a Paperclip company skill for Twenty execution work:

1. Read the related Paperclip issue and blockers through `paperclip-admin` rules.
2. Draft only the company-skill content locally unless the operator approves a Paperclip mutation.
3. Keep the execution skill narrower than this operator skill: it should teach engine agents the CRM operations they need, not Paperclip administration.
4. Include dry-run, idempotency, identity precedence, guarded-field handling, approval boundaries, readback verification, and no-outreach/no-credit-spend constraints.
5. If the draft depends on unresolved schema details, mark those as blocked assumptions instead of inventing fields.

Do not install, attach, or update the Paperclip company skill library from this branch. That is a Paperclip mutation and must route through `paperclip-admin` with explicit approval.

## Output

Report the operational facts:

- objects and identity keys processed
- tool operations used
- counts read
- per-record result: `matched-updated(id)`, `created(id)`, `collision-skipped`, or `blocked`
- dry-run versus live write
- field diffs and guarded fields left unchanged
- unique constraint relied on, if any upsert was used
- errors, missing fields, unresolved blockers, and follow-up decisions
