---
name: paperclip-source-capture
description: Capture a creator's raw brain-dump into their LLM Wiki space as a no-task raw source, then run guided ingest into structured, durable wiki pages. Use when someone wants to dump ideas, record content source material, or brief a space that other agents will later read with wiki-ask. Operator/privileged path — bypasses the shared Wiki Maintainer.
---

# Paperclip Source Capture

Run a creator's source-capture loop directly against their LLM Wiki space:

```text
Raw dump (raw/, no task)  ->  guided ingest (structured wiki/ pages, no maintainer)  ->  reused via wiki-ask
```

This skill **captures and ingests only**. It never publishes, schedules, posts, or anonymizes. Anonymization happens later, at publish time, in the agent that drafts the public artifact.

## Why this skill (and not the default wiki flow)

The wiki's default file-upload path creates a per-file ingest **operation issue** and hands it to the shared **Wiki Maintainer** agent. That leaves task trace and can't be tuned per creator. This skill instead writes straight to the space through the **no-task** plugin routes (verified below), so the operator owns the loop end to end and the Maintainer is never invoked.

Relationship to the company `wiki-ask` / `wiki-contribute` skills (worker-agent path):
- `wiki-contribute` deposits to the **default** space and walks away for the Maintainer to curate. This skill is the **operator** equivalent aimed at a **creator's own space**, and it does the ingest itself.
- `wiki-ask` is how a downstream agent (e.g. a post writer) later **reads** the space. Reference it by name; it lives in the company skill library.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/paperclip-operator/cli-contract.md` (wiki route sections)
- `references/docs/paperclip-operator/integration-matrix.md`

## Inputs (resolve before any write)

- **`spaceSlug`** — required. **Prompt the creator for it every run.** Never assume a default. Confirm it exists with the spaces route; if it does not, stop and ask the operator to create it (a space is board-created; see Route Contract).
- **`companyId`**, **`wikiId`** (`default`) — derive from `paperclipai context show --json`. Use the creator's own company.

Echo the resolved `spaceSlug` + `companyId` back before writing.

## Modes

### Raw capture (verbatim, lossless, no task)

The safety net. Saving raw is consented by invoking the skill — do it immediately, do not editorialize.

1. **On invocation**, write the creator's first message verbatim as a raw source via the capture route. Rough is fine; preserve voice; do not edit or anonymize.
2. Use a clear `title` (it becomes the filename stem) and `metadata` (`{capturedBy, context}`).
3. The route writes the file under the space's `raw/` and returns `{sourceId, rawPath, hash}`. Report `rawPath`.
4. **After guided ingest finishes, prompt:** "Dump the whole conversation to the raw file?" On approval, write the full transcript as a second raw source. This step is explicit-approval, not automatic.

### Guided ingest (clarify-style, structured, no maintainer)

Turn the raw dump into durable, cited pages — behaving like `paperclip-clarify` / `record-strategy`.

1. Read existing space content first (pages + sources routes) so you extend rather than clobber.
2. Ask the creator clarifying questions to organize the raw into durable knowledge.
3. Draft structured pages into the wiki categories: `wiki/sources/`, `wiki/concepts/`, `wiki/entities/`, `wiki/synthesis/` (subdirs are conventional; add categories as the domain needs).
4. **Present each proposed page (path + full body) and get approval**, then write it via the `write-page` action (no task). Use `expectedHash` when updating an existing page; re-read and stop on hash conflict.
5. Keep the wiki internal and rich. **Do not anonymize here** — that is the publish-stage agent's job.
6. Read each page back and verify path, title, and hash before reporting done.

## Route Contract (verified)

All routes are on the LLM Wiki plugin. Two path forms:
- **Direct REST / curl** (bearer auth): `{API}/api/plugins/paperclipai.plugin-llm-wiki/...`
- **MCP `paperclipApiRequest`** (board/operator): **drop the leading `/api`** — it is added by the MCP. (Passing `/api/...` yields `/api/api/...` → 404.)

Operator skills run as **board**, so they may call board and board-or-agent routes.

| Purpose | Method + path (REST form) | Body | Task? |
|---|---|---|---|
| List spaces | `GET …/api/plugins/…llm-wiki/api/spaces?companyId=&wikiId=default` | — | no |
| Create space (board) | `POST …/api/plugins/…llm-wiki/api/spaces` | `{companyId,wikiId,slug,displayName,folderMode,accessScope}` | no |
| **Raw capture** | `POST …/api/plugins/…llm-wiki/api/sources` | `{companyId,wikiId,spaceSlug,sourceType:"text",title,contents,url?,metadata?}` | **none** ✅ |
| **Write page** | `POST …/api/plugins/…llm-wiki/actions/write-page` | `{companyId,params:{wikiId,spaceSlug,path,contents,expectedHash?,summary?}}` | **none** ✅ |
| List raw sources | `POST …/api/plugins/…llm-wiki/data/sources` | `{params:{companyId,wikiId,spaceSlug,limit?}}` | no |
| List pages | `POST …/api/plugins/…llm-wiki/data/pages` | `{params:{companyId,wikiId,spaceSlug,includeRaw?}}` | no |
| Read page body | `POST …/api/plugins/…llm-wiki/data/page-content` | `{params:{companyId,wikiId,spaceSlug,path}}` | no |
| List operations (audit) | `GET …/api/plugins/…llm-wiki/api/operations?companyId=&wikiId=&spaceSlug=` | — | no |

**Do not use** `…/api/file-as-page` for ingest — it writes the page but also creates a (done) `file-as-page` **operation issue**, leaving the trace this skill exists to avoid. Use `actions/write-page`.

`captureWikiSource` and `writeWikiPage` are verified to create no operation, comment, event, or wakeup.

## Mutation Rule

- Raw capture of the creator's own input is consented by invocation — write it immediately.
- Every structured-page write and the full-conversation dump require **explicit approval**: present the exact path + body, write only what is approved, then read back and verify.
- Never anonymize, publish, or call the Wiki Maintainer from this skill. Never print bearer tokens.
