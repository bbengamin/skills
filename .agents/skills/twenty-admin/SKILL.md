---
name: twenty-admin
description: Operate Twenty CRM (the sales system of record) directly as the operator agent. Use when the user wants to read or write Twenty data — query people/companies/campaigns/opportunities by identity, idempotent match-or-create, non-destructive updates, schema/metadata inspection. Self-contained: it knows where the Twenty MCP lives and how to drive it. Reads freely; asks before any mutation; never touches SDR-owned structures; no outreach or deletes without explicit approval.
---

# Twenty Admin

Operate Twenty CRM directly through the approved MCP, with the connection details, access pattern, object model, and guardrails baked in so the operator never has to re-explain them.

Twenty is the **system of record for sales/CRM** at Right.Link. It is shared with live SDR work, so the default posture is: read freely, treat writes as risky, and stay strictly additive and non-destructive.

## When To Use

- Reading or writing Twenty records (people, companies, campaigns, opportunities, notes, tasks).
- Identity-based lookup and idempotent match-or-create.
- Inspecting Twenty object/field metadata (schema audit, gap mapping).

Route elsewhere when:
- The request is Paperclip control-plane work → `paperclip-admin` and the paperclip suite.
- It is outbound planning/triage/strategy → the `outbound-*` / `growth-*` skills (those plan work; this one executes Twenty reads/writes).
- It involves sending outreach, enrichment spend, or sequencing → those are gated and belong to the dedicated channel tools (grinfi/instantly/Clay), not routine CRM ops here.

## Where Twenty Lives (no need to ask)

Twenty is exposed through the **metamcp** aggregator under the `twenty` namespace. Tools are named `mcp__metamcp__twenty__*`.

- MCP server `metamcp` in `.mcp.json`: native SSE to `https://metamcp.dev.right.link/metamcp/sales/sse` with an `Authorization: Bearer <token>` header (token already in the file).
- The same metamcp server also exposes `grinfi`, `instantly`, `composio`, `Postiz` namespaces.

If the `mcp__metamcp__twenty__*` tools are not present:
1. `claude mcp list` — confirm `metamcp` shows `✔ Connected`.
2. If it failed: the entry must be native SSE with a Bearer header — **not** `mcp-proxy` (that package is a stdio→SSE *server* wrapper and will treat the URL as a command to spawn). Correct shape:
   ```json
   "metamcp": { "type": "sse", "url": "https://metamcp.dev.right.link/metamcp/sales/sse", "headers": { "Authorization": "Bearer <token>" } }
   ```
3. Config changes need a Claude Code restart / new session before tools appear.

## Access Pattern (meta-tool indirection)

Twenty is driven through a small set of meta-tools — do not guess concrete tool names:

1. `mcp__metamcp__twenty__list_object_metadata_names` — quick connectivity + object list.
2. `mcp__metamcp__twenty__get_tool_catalog` — browse operations by category (start here; the catalog is the source of truth).
3. `mcp__metamcp__twenty__learn_tools` — get the exact input schema for the operations you intend to run (pass all needed names in one call).
4. `mcp__metamcp__twenty__execute_tool` — run an operation by exact name with arguments matching the learned schema.

Built-in Twenty playbooks are available via `list_skills` / `load_skills` (e.g. `data-manipulation`, `metadata-building`); load them when a task matches.

## Object Model & Identity

Workspace has ~22 objects. Core for outbound: `people`, `companies`, `campaigns`, `opportunities`, `notes`, `tasks`.

Identity keys for a Person (precedence order):
1. `linkedinLink.primaryLinkUrl`
2. `emails.primaryEmail`

Two records are the same person if either key matches. Person also has `companyId` and a direct `campaignId` relation.

**Do-not-touch (SDR-owned), pending the RL-434 audit:** custom Person relations `interestedInId`, `notInterestedInId`, `n5050Id`, and any existing campaign structure the SDRs rely on. Never write these without explicit approval. Run a fresh `get_object_metadata` / `get_field_metadata` audit to finalize the list before non-trivial writes.

## Operation Vocabulary

Per object, DATABASE_CRUD operations follow a fixed naming pattern:
`find_many_<plural>`, `find_one_<singular>`, `group_by_<plural>`, `create_one_<singular>`, `create_many_<plural>`, `update_one_<singular>`, `update_many_<plural>`, `upsert_many_<plural>`, `delete_one_<singular>`, `delete_many_<plural>`.

Other categories: METADATA (`get_object_metadata`, `get_field_metadata`, `create_field_metadata`, `create_many_relation_fields`, …), ACTION (`send_email`, `draft_email`, `search_help_center`, `navigate_app`), WEBHOOK, VIEW, DASHBOARD, LOGIC_FUNCTION.

## Query Syntax Essentials

- `select` is **required** on `find_*` (use `"*"` for all, or list fields). MANY_TO_ONE relations are read via their FK column (e.g. `companyId`).
- Filter fields are **top-level keys**, each its own operator object — e.g. `{ "emails": { "primaryEmail": { "eq": "a@b.com" } } }`. Do NOT wrap in a `filter` object; do NOT put a bare `eq`/`ilike` at the top level.
- Combine with `and` / `or` / `not` arrays.
- `orderBy`: scalar `[{ "employees": "DescNullsLast" }]`; composite `[{ "name": { "firstName": "AscNullsFirst" } }]` — never dot-notation.

## Idempotent Match-Or-Create

For each input record:
1. `find_many_<object>` by identity key(s), with `select`.
2. 0 matches → `create_one_<object>`.
3. 1 match → `update_one_<object>` by `id`, additive only.
4. >1 match → do not write; report a duplicate collision for human resolution.

`upsert_many_<object>` (max 20/call) matches only on **unique-constrained** fields. Standard email/linkedin fields are not unique by default, so use upsert for identity dedup only after confirming a backing unique constraint (an additive metadata change from the audit).

## Operating Loop

1. Confirm connectivity (`list_object_metadata_names`).
2. Inspect current Twenty state before changing anything (metadata + `find_*`).
3. Decide read-only vs mutating.
4. Read-only → answer directly with records + uncertainty.
5. Mutating → present the exact planned change (per-record would-create / would-update + field diff) and wait for approval.
6. Apply only the approved change.
7. Read the record back (`find_one_*`) and verify the written fields.
8. Report what changed, record ids, and anything still needing attention.

## Mutation & Approval Boundary

Read freely. Ask before any create / update / upsert. Default writes to **dry-run** (resolve and show the planned diff) and execute live only after approval.

Especially explicit approval required for: any `delete_*`; writes onto or near SDR-owned objects/fields; overwriting a populated field or shrinking a multi-value field; any METADATA/schema change; any ACTION that contacts a person or spends credits (`send_email`, `draft_email`, enrichment).

Never silently overwrite, delete, or touch SDR structures. When identity is ambiguous, stop and ask.

## Common Reads

- `list_object_metadata_names` — objects in the workspace.
- `get_tool_catalog` (categories: `["DATABASE_CRUD"]`, `["METADATA"]`) — available ops.
- `find_many_people` with `select` and an identity filter — look up a contact.
- `get_object_metadata` / `get_field_metadata` — schema audit / gap mapping.

## Common Writes (after approval)

- `create_one_person` / `update_one_person` — additive golden-record write via match-or-create.
- `upsert_many_people` — batch idempotent write, only when a unique key backs the identity field.
- `create_field_metadata` — additive, namespaced field for the extension plan (audit/extension work, not routine ops).

## Output

After any operation, report: objects + identity keys processed; counts read; per-record matched-updated(id) / created(id) / collision-skipped with field diff; dry-run vs live; unique-constraint relied on if upsert used; errors, missing fields, and do-not-touch violations avoided.
