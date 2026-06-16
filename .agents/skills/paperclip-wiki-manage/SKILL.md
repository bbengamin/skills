---
name: paperclip-wiki-manage
description: Manage Paperclip llm-wiki content through confirmed plugin bridge REST write routes with strict mutation approval. Use when the agent needs to create, update, rename, archive, delete, or otherwise mutate Paperclip wiki pages or captured wiki sources, and must verify routes, show exact proposed changes, get operator approval, and read back results.
---

# Paperclip Wiki Manage

Manage Paperclip llm-wiki content only through confirmed `paperclipai.plugin-llm-wiki` plugin bridge write routes.

Use `paperclip-wiki-fetch` for read-only page content, page lists, source lists, and SPA URL path conversion. Use this skill only for wiki mutations.

## Path forms and the MCP gotcha

- **Action bridge** (write): `/api/plugins/paperclipai.plugin-llm-wiki/actions/<key>`, body `{ "companyId": "...", "params": { ... } }`.
- **Scoped REST** (write): `/api/plugins/paperclipai.plugin-llm-wiki/api/<route>` (extra `/api` segment), flat JSON body.

When calling through MCP `paperclipApiRequest`, **omit the leading `/api`** — the MCP prepends it; `/api/plugins/...` becomes `/api/api/...` → `404`. Direct REST / curl uses the full `/api/plugins/...` path with a bearer token.

## Confirmed Route Requirement

Do not guess wiki write routes. Verified routes (each confirmed to create **no operation/task** unless noted):

```text
POST /api/plugins/paperclipai.plugin-llm-wiki/actions/write-page   # write/replace a page directly — NO task ✅
POST /api/plugins/paperclipai.plugin-llm-wiki/api/sources          # capture a raw source into raw/ — NO task ✅
POST /api/plugins/paperclipai.plugin-llm-wiki/api/spaces           # create a space (board)
```

**Avoid `…/api/file-as-page`**: it writes a page but also creates a (auto-completed) `file-as-page` **operation issue**, leaving task trace. For a clean direct page write use `actions/write-page`.

Use `actions/write-page` to write a markdown page. Verified body shape:

```json
{
  "companyId": "<company-id>",
  "params": {
    "wikiId": "default",
    "spaceSlug": "<space-slug>",
    "path": "wiki/sources/example.md",
    "contents": "# Example\n",
    "expectedHash": "<optional-current-hash>",
    "summary": "<optional-change-summary>"
  }
}
```

Use `api/sources` to deposit a raw source (the same primitive the `wiki-contribute` skill uses). Flat body `{companyId, wikiId, spaceSlug, sourceType:"text", title, contents, url?, metadata?}`; returns `{sourceId, rawPath, hash}`. This lands in the space's `raw/` with status `captured` and does **not** trigger the Wiki Maintainer.

**Spaces:** writes target a `spaceSlug` (default `default`; per-creator/team spaces exist, e.g. `creator-jane`). List them via the fetch skill's `api/spaces` route. Paths inside a space are relative (`wiki/...`, `raw/...`).

When using another wiki mutation route, identify a confirmed plugin bridge write route and schema from one of:

- official Paperclip/plugin docs
- inspected Paperclip/plugin source code
- an operator-provided working example
- a successful non-mutating schema/options/read probe that proves the route contract

The route must be under one of:

```text
/api/plugins/paperclipai.plugin-llm-wiki/data/...
/api/plugins/paperclipai.plugin-llm-wiki/actions/...
```

Never use `/api/wiki/...` and never infer write routes by renaming read routes.

## Mutation Workflow

1. Classify the requested mutation:
   - create page
   - update page body or title
   - move or rename page path
   - archive or delete page
   - create, update, archive, or delete captured source
   - another plugin-supported wiki mutation
2. Inspect Paperclip context and auth without printing secrets.
3. Fetch current wiki state with `paperclip-wiki-fetch`:
   - list pages or sources when choosing a target
   - fetch page content before editing an existing page
   - record title, path, update time, and hash when available
4. Confirm the exact write route, HTTP method, and request schema. For page writes, use `POST /api/plugins/paperclipai.plugin-llm-wiki/actions/write-page`.
5. Draft the exact proposed mutation:
   - target company, wiki, space, route, and path
   - request JSON with secrets omitted
   - markdown diff for page body changes, or full body when creating a page
   - expected title, path, page type, source metadata, and hash/update behavior
6. Ask for explicit operator approval before the write.
7. Immediately before writing, re-fetch the target page or source when it already exists.
8. If the update time or hash changed since approval, stop and ask whether to rebase the edit.
9. Apply only the approved mutation through the confirmed plugin bridge route.
10. Read the page or source back and verify:
    - title
    - path
    - body or source metadata
    - page type, when available
    - update time
    - hash
11. Report the route used, record identifiers, verification result, and any remaining uncertainty.

## Approval Rules

- Ask before every create, update, move, rename, archive, delete, source capture, or source mutation.
- Destructive operations require especially explicit approval that names the target path/source and action.
- Do not combine multiple wiki mutations into one approval unless the operator approved the exact batch.
- Do not mutate Paperclip issues, goals, projects, agents, or approvals from this skill unless another skill's approved workflow explicitly calls for it.

## Failure Handling

- If no confirmed write route exists, stop and report that wiki management is blocked on route/schema discovery.
- If auth, company id, wiki id, space slug, page path, or target source id is missing and cannot be inferred, ask for the missing input.
- If readback does not match the intended mutation, report the mismatch and do not perform follow-up repair without fresh approval.
- If the requested operation would publish sensitive, secret, or unapproved external content, stop and ask for operator review.

## Safe Defaults

- Default `wikiId` to `default` only when the existing wiki context or user prompt supports it.
- Default `spaceSlug` to `default` only when the existing wiki context or user prompt supports it.
- Preserve existing page path and title unless the operator explicitly requested a rename or move.
- Prefer small targeted edits over replacing an entire page.
- Keep Paperclip plan documents as the source of truth unless the operator explicitly asks to publish or sync content to wiki.
