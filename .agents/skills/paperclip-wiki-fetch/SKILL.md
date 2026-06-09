---
name: paperclip-wiki-fetch
description: Fetch Paperclip llm-wiki content through the plugin bridge REST API. Use when the agent needs to read a Paperclip wiki page, list wiki pages, list captured wiki sources, convert a Paperclip wiki SPA URL into an API request, or retrieve markdown from paperclipai.plugin-llm-wiki.
---

# Paperclip Wiki Fetch

Fetch Paperclip wiki data through the `paperclipai.plugin-llm-wiki` plugin bridge API.

Use this skill for read-only wiki retrieval. Do not use `/api/wiki/...`; llm-wiki exposes data through plugin bridge routes under `/api/plugins/paperclipai.plugin-llm-wiki/data/...`.

## Inputs

Identify these values before calling the API:

- Paperclip API base URL, for example `https://paperclip.right.link`
- bearer token in an environment variable such as `TOKEN`
- `companyId`
- `wikiId`, usually `default`
- `spaceSlug`, usually `default`
- page `path`, for example `wiki/sources/rl-30-day-validation-plan.md`

If a user gives a public-looking wiki URL, treat it as an SPA route and extract the page path from it. For example:

```text
https://paperclip.right.link/RL/wiki/page/wiki/sources/rl-30-day-validation-plan.md
```

maps to:

```text
wiki/sources/rl-30-day-validation-plan.md
```

Do not include the company slug prefix, `/wiki/page/`, query string, or fragment in the `path`.

## Routes

Use these plugin bridge routes:

```text
POST /api/plugins/paperclipai.plugin-llm-wiki/data/page-content
POST /api/plugins/paperclipai.plugin-llm-wiki/data/pages
POST /api/plugins/paperclipai.plugin-llm-wiki/data/sources
```

`data/page-content` returns the page markdown body plus metadata such as title, page type, update time, and hash.

`data/pages` lists wiki pages.

`data/sources` lists captured raw sources.

## Request Shape

Send JSON with a top-level `params` object:

```json
{
  "params": {
    "companyId": "0f54ac28-6909-4c63-afec-14321af7c21b",
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
  "https://paperclip.right.link/api/plugins/paperclipai.plugin-llm-wiki/data/page-content" \
  -d '{
    "params": {
      "companyId": "0f54ac28-6909-4c63-afec-14321af7c21b",
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
  "https://paperclip.right.link/api/plugins/paperclipai.plugin-llm-wiki/data/pages" \
  -d '{
    "params": {
      "companyId": "0f54ac28-6909-4c63-afec-14321af7c21b",
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
  "https://paperclip.right.link/api/plugins/paperclipai.plugin-llm-wiki/data/sources" \
  -d '{
    "params": {
      "companyId": "0f54ac28-6909-4c63-afec-14321af7c21b",
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
