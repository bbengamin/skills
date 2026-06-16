---
name: paperclip-wiki-fetch
description: Fetch Paperclip llm-wiki content through the plugin bridge REST API. Use when the agent needs to read a Paperclip wiki page, list wiki pages, list captured wiki sources, convert a Paperclip wiki SPA URL into an API request, or retrieve markdown from paperclipai.plugin-llm-wiki.
---

# Paperclip Wiki Fetch

Fetch Paperclip wiki data through the `paperclipai.plugin-llm-wiki` plugin bridge API.

Use this skill for read-only wiki retrieval. Do not use `/api/wiki/...`; llm-wiki exposes data through plugin bridge routes under `/api/plugins/paperclipai.plugin-llm-wiki/data/...`.

## Inputs

Identify these values before calling the API:

- Paperclip API base URL, for example `https://your-paperclip-host.example.com`
- bearer token in an environment variable such as `TOKEN`
- `companyId`
- `wikiId`, usually `default`
- `spaceSlug` — `default` unless a specific space is named; list spaces with the `api/spaces` route
- page `path`, for example `wiki/sources/rl-30-day-validation-plan.md`

If a user gives a public-looking wiki URL, treat it as an SPA route and extract the page path from it. For example:

```text
https://your-paperclip-host.example.com/<company-slug>/wiki/page/wiki/sources/rl-30-day-validation-plan.md
```

maps to:

```text
wiki/sources/rl-30-day-validation-plan.md
```

Do not include the company slug prefix, `/wiki/page/`, query string, or fragment in the `path`.

## Path forms

The plugin mounts two surfaces. Get the prefix right or every call 404s:

- **Generic data bridge** (read): `/api/plugins/paperclipai.plugin-llm-wiki/data/<key>`, JSON body `{ "params": { ... } }`.
- **Scoped REST routes**: `/api/plugins/paperclipai.plugin-llm-wiki/api/<route>` (note the extra `/api` segment), flat JSON body or query string.

**MCP gotcha:** when calling through MCP `paperclipApiRequest`, **omit the leading `/api`** (the MCP prepends it). Passing `/api/plugins/...` becomes `/api/api/plugins/...` → `404 API route not found`. Direct REST / curl uses the full `/api/plugins/...` path with a bearer token.

## Routes

Read via the data bridge (`{ "params": { ... } }` body):

```text
POST /api/plugins/paperclipai.plugin-llm-wiki/data/page-content   # page markdown body + title, pageType, updatedAt, hash
POST /api/plugins/paperclipai.plugin-llm-wiki/data/pages          # list wiki pages (optional includeRaw)
POST /api/plugins/paperclipai.plugin-llm-wiki/data/sources        # list captured raw sources (rawPath, title, status)
```

Scoped REST reads (query string, not `params`):

```text
GET  /api/plugins/paperclipai.plugin-llm-wiki/api/spaces?companyId=<id>&wikiId=default      # list wiki spaces
GET  /api/plugins/paperclipai.plugin-llm-wiki/api/operations?companyId=<id>&spaceSlug=<s>   # list ingest/query/lint operations
```

All read routes are `board-or-agent`.

## Spaces

The wiki is partitioned into **spaces** (slug-prefixed folders under the wiki root). `spaceSlug` defaults to `default`, but per-creator/per-team spaces exist (e.g. `creator-jane`, with `pathPrefix: spaces/<slug>`). List them with the `api/spaces` route. Pass the intended `spaceSlug` on every read; omitting it targets `default`. Paths inside a space are relative (`wiki/sources/foo.md`, `raw/...`), not prefixed with `spaces/<slug>`.

## Request Shape

Send JSON with a top-level `params` object:

```json
{
  "params": {
    "companyId": "<company-id>",
    "wikiId": "default",
    "spaceSlug": "default",
    "path": "wiki/sources/rl-30-day-validation-plan.md"
  }
}
```

For `data/pages` and `data/sources`, omit `path` unless the API specifically supports filtering for the requested task.

## Curl Examples

Fetch page content:

```sh
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://your-paperclip-host.example.com/api/plugins/paperclipai.plugin-llm-wiki/data/page-content" \
  -d '{
    "params": {
      "companyId": "<company-id>",
      "wikiId": "default",
      "spaceSlug": "default",
      "path": "wiki/sources/rl-30-day-validation-plan.md"
    }
  }'
```

List pages:

```sh
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://your-paperclip-host.example.com/api/plugins/paperclipai.plugin-llm-wiki/data/pages" \
  -d '{
    "params": {
      "companyId": "<company-id>",
      "wikiId": "default",
      "spaceSlug": "default"
    }
  }'
```

List captured sources:

```sh
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://your-paperclip-host.example.com/api/plugins/paperclipai.plugin-llm-wiki/data/sources" \
  -d '{
    "params": {
      "companyId": "<company-id>",
      "wikiId": "default",
      "spaceSlug": "default"
    }
  }'
```

## Operating Rules

- Read freely when the user asks for wiki data and credentials are already available.
- Do not print bearer tokens or write them into files.
- Prefer `paperclipai context show --json` to discover API base and company id when the CLI is configured.
- Ask for the missing company, wiki, space, page path, or token source only when it cannot be inferred from context.
- If a wiki request returns a list, inspect titles, paths, update times, and hashes before choosing a page.
- If a page fetch fails, verify the route is the plugin bridge route, the page path excludes the SPA prefix, and the request body uses `params`.
- Treat this API as read-only unless explicit write routes are added and the operator approves a mutation workflow.
