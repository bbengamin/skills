---
name: paperclip-source-capture
description: Capture raw founder, builder, or creator source material into a Paperclip issue's raw-log document, then distill it into anonymized, tagged, post-ready snippets. Use when someone wants to brain-dump, record ideas, or dump source material for content that other agents will reuse later.
---

# Paperclip Source Capture

Run a two-stage material capture loop on a Paperclip issue, storing everything in keyed issue documents so any agent that later picks up the issue can read it:

```text
Dump (raw, dated)  ->  Distill (anonymized, tagged snippets)  ->  reused by campaigns/posts
```

This skill captures and distills only. It does not plan, publish, schedule, or take any platform action.

## Why issue documents, not the wiki

Captured material lives in the issue's own keyed documents (`paperclipUpsertIssueDocument` / `paperclipGetDocument`), not in the llm-wiki. Normal worker agents cannot read llm-wiki content through an agent-safe route today (the plugin stream bridge is board/UI-only; granting wiki tools to worker agents is too broad). An issue's documents, by contrast, are part of the context an assigned agent reads at checkout/heartbeat. So issue documents are the only store reliably readable by the agent that later reuses the material. Do not move this store to the wiki unless an agent-safe wiki read route exists and the operator approves the change.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/paperclip-operator/control-plane.md`
- `references/docs/paperclip-operator/workflow.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

If these project docs are missing, run `paperclip-setup` first to scaffold them from bundled templates.

## Capture Target

This skill is not hardcoded to one person or issue. Resolve the target before any read or write:

- **Capture issue** — the Paperclip issue that owns the material loop. Take an explicit issue id or identifier from the operator when given.
- **Raw-log document key** — default `founder-log`.
- **Distilled-material document key** — default `founder-material`.

Resolution order:

1. If the operator names an issue, use it. Confirm it exists with `paperclipGetIssue` and read its `documentSummaries` to see which keyed documents are present.
2. If the operator does not name an issue, list candidate capture issues (e.g. issues titled like a material capture loop in the relevant project) and ask which one. Do not guess.
3. If the chosen issue has no raw-log or material document yet, propose creating them from the templates in **Document Formats** below, and create them only after approval.
4. If no capture issue exists at all, propose creating one (`backlog`, unassigned) to own the loop, then propose its two documents. Create only after approval.

Always echo the resolved issue identifier and document keys back before mutating.

## Process

1. Resolve the **Capture Target** (issue + log key + material key).
2. Read the current raw-log and material documents with `paperclipGetDocument`. Never write blind over an existing document.
3. Pick the mode the operator wants: **Dump**, **Distill**, or both.
4. Draft the exact new document body (full body, not a vague summary of the change).
5. Present the proposed change and wait for approval (see **Mutation Rule**).
6. Write only the approved body with `paperclipUpsertIssueDocument`.
7. Read the document back and verify the new revision contains the intended content.
8. Report the issue, document key, new revision number, and a one-line summary of what was added.

## Dump Mode

Capture raw material with minimal friction and zero editorializing.

- Accept whatever the contributor provides: pasted text, transcript, rough bullets, links, half-formed ideas. Rough is fine and expected.
- **Preserve the raw voice. Do not rewrite, polish, summarize, or anonymize in this mode.** The raw log is the unfiltered source.
- Prepend a new dated entry to the top of the raw-log body (newest first), using the entry format in **Document Formats**.
- Use the contributor-supplied date if given, otherwise today's date in `YYYY-MM-DD`. Add a short human label.
- Keep the document's header/banner and the `<!-- Append ... -->` guide comment intact; insert the new entry directly beneath the guide comment, above any existing entries.
- The raw log is internal. It carries a "do not publish verbatim" banner. Never treat raw-log text as publishable output.

## Distill Mode

Promote new raw entries into anonymized, tagged, post-ready snippets in the material document. This mode carries operator judgment — slow down here.

- Read the raw-log entries that are not yet represented in the material document. Work from the raw source, not from memory.
- For each distillable idea, produce one snippet in the format in **Document Formats**: anonymized text, supporting post angle(s), a confidence flag, and a source pointer back to the raw-log date/label.
- Number snippets continuously (`S<n>`); continue from the highest existing number in the material document. Do not renumber existing snippets.
- **Anonymization is a hard rule.** A distilled snippet must contain none of:
  - client, customer, carrier, partner, or employer names
  - named internal systems or products
  - exact volumes, revenue figures, counts, or dates that pin down a specific deal
  - combinations of details that together identify a real person or company even when each detail alone seems safe
- Keep the founder/builder voice. Distilled material is natural first-person reflection, not product marketing.
- Set `Confidence`:
  - `solid` — the underlying raw material clearly supports the claim.
  - `thin` — plausible but under-supported; flag it so downstream drafting treats it carefully.
  - `unsupported` — the angle is interesting but the raw log does not actually back it; keep it flagged, do not present it as fact.

### Stop Conditions

Stop and ask the operator instead of writing when:

- a snippet could identify a real person or company even after your anonymization pass,
- the raw material is too thin to support the claim a snippet would make, or
- distillation is drifting into salesy positioning rather than honest founder/builder reflection.

When in doubt, leave the idea in the raw log and flag it rather than publishing a risky snippet to the material document.

## Document Formats

Honor these formats exactly so downstream agents and existing tooling can parse the store. When creating a fresh capture issue's documents, seed them with these templates.

Raw-log document (default key `founder-log`):

```markdown
# <Raw log title>

> INTERNAL RAW SOURCE. Dated dumps of <whose> founder/builder story and updates. Rough is fine. Distilled, anonymized snippets live in the `<material-key>` document. Do not publish anything from this document verbatim.

<!-- Append new entries below, newest first, as: ## YYYY-MM-DD — short label -->

## YYYY-MM-DD — short label

<raw, unedited dump>
```

Distilled-material document (default key `founder-material`):

```markdown
# <Material title> (distilled, anonymized, tagged)

Post-ready snippets distilled from the `<log-key>` document. Anonymization is a hard rule: no client/customer/carrier names, named systems, exact volumes, or identifying combinations. Each snippet is tagged with the post angle(s) it can support and flagged if thin or unsupported. Campaign bundles cite from here.

<!-- Snippet format:
### S<n> — <short label>
- Snippet: <anonymized, post-ready text>
- Angle(s): <post angle tags>
- Confidence: solid | thin | unsupported
- Source: <log-key> <date/label>
-->

### S<n> — <short label>
- Snippet: <anonymized, post-ready text>
- Angle(s): <post angle tags>
- Confidence: solid | thin | unsupported
- Source: <log-key> <date/label>
```

## Surface Rules

Read `cli-contract.md` and `integration-matrix.md` before choosing tools. For this skill:

- Reads — prefer CLI `paperclipai issue get --json` for the issue; use MCP `paperclipGetIssue`, `paperclipListDocuments`, and `paperclipGetDocument` for documents and their revisions.
- Writes — keyed issue documents are the store. Use MCP `paperclipUpsertIssueDocument` (and `paperclipCreateIssue` only when creating a new capture issue) when the CLI lacks native document commands.
- Use `paperclipApiRequest` only for an operation missing from both CLI and dedicated MCP tools, and direct REST only when CLI and MCP are unavailable or broken.
- Never embed the captured material anywhere other than the issue's keyed documents. Do not duplicate it into the issue description, a comment, a local file, or the wiki as the source of truth.
- Never print bearer tokens. If auth cannot be derived, stop and ask for context rather than degrading the capture.

## Mutation Rule

Writing to a capture document mutates the control plane. Always:

1. Read the current document body first.
2. Present the full proposed new body (or the exact entry/snippet being prepended) in chat as plain text.
3. Wait for explicit operator approval.
4. Write only the approved body.
5. Read the document back and verify the new revision before reporting done.

Read-only inspection of capture issues and documents does not need approval.
