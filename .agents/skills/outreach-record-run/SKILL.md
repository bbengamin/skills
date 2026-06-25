---
name: outreach-record-run
description: Materialize an approved Outreach Run Spec into a Paperclip Run Record and initialize its checkpoint, one run at a time. Use after outreach-clarify when the operator approves recording or updating a run, or wants to start or resume the Run Record for an outbound-engine run before any stage executes.
---

# Outreach Record Run

Record an approved Outreach Run Spec as a Paperclip Run Record, or update an existing one. This is the first mutating step of the operations plane. Mutate Paperclip only; do not run any stage and do not write to Twenty.

## References

Read these first:

- `references/CONTEXT.md`
- `references/docs/outreach-operator/workflow.md`
- `references/docs/outreach-operator/control-plane.md`
- `references/docs/paperclip-operator/cli-contract.md`
- `references/docs/paperclip-operator/integration-matrix.md`

Open when locating the upstream campaign or project:

- `references/docs/growth-operator/control-plane.md`

## Process

1. Confirm an approved Outreach Run Spec.
   - If `outreach-clarify` produced one in-thread and the operator approved it, treat it as approved.
   - If the operator asks to record a run without a spec, first produce a concise Run Spec from resolved answers and get approval before mutating.
   - Done when the campaign, stage scope, ICP filters, list scope, tools, caps, gates, and stop conditions are all settled.
2. Inspect current Paperclip state: the approved campaign or strategy parent, its project and goals, and any existing Run Record under it.
3. Decide new versus resume.
   - No Run Record for this campaign and stage scope: create one.
   - A Run Record exists: update it, and never reset a stage already past `pending` without the operator's explicit approval.
   - Done when you can name the one Run Record this run writes to.
4. Draft the exact proposed mutation: the run issue fields and the Run Record plan-document body, with the stage checklist initialized.
5. Ask for approval before mutating Paperclip.
6. Apply only approved changes, one dependency at a time: create the run issue, then put its Run Record document. Verify each write before the next.
7. Read back the run issue and document, and report identifiers.
8. Initialize the checkpoint: every in-scope stage at `pending`, out-of-scope stages omitted. Do not set any stage to `running`; starting a stage is a stage-runner action, not a record-run action.

## Run Record As Paperclip

Materialize the Run Record as a child run issue under the approved campaign, carrying a single plan document keyed `outreach-run`. The document is the durable run state and the home of the stage checklist; later checkpoints update this document.

- Title the run issue for the run, for example `Run: enrich June logistics batch`.
- Link it to the campaign parent and the campaign's project.
- Record the Twenty segment as a pointer (filter or saved-view reference), not as copied lead data.
- Keep the run issue unassigned and unstarted; record-run records intent, it does not start work or move the issue to `todo`.

## Run Record Plan Document

Recommended shape, mapping onto `control-plane.md`:

```markdown
## Campaign

## Stage Scope

## ICP Slice And Filters

## Twenty Segment Pointer

## Tools Per Stage

## Enrichment Waterfall

## Output Definition

## Caps

## Suppression And Compliance

## QA Gates

## Success Signal And Stop Conditions

## Stage Checklist
- source: pending
- resolve: pending
- enrich: pending
- gate: pending
- assemble: pending
- push: pending
```

List only in-scope stages in the checklist. When updating an existing Run Record, edit the existing document and add a comment summarizing what changed and why. Create a new run issue only for a distinct run.

## Wiki Source Material

When the approved spec or campaign references a Paperclip wiki page or captured source for ICP or proof, use `paperclip-wiki-fetch` before drafting the document, and record the fetched title, path, update time, and hash. If wiki access details are missing and cannot be inferred, stop and ask rather than drafting from an unfetched reference. If the operator asks to publish the run artifact to wiki, finish the Paperclip Run Record first, then use `paperclip-wiki-manage`.

## Surface Rules

Use the CLI-first ladder in `integration-matrix.md`: CLI when it supports and verifies the native field, dedicated MCP tools when CLI is insufficient, `paperclipApiRequest` when no dedicated tool exists, and direct REST only when CLI and MCP are unavailable.

Before any MCP API request or direct REST mutation, derive API base and company from `paperclipai context show --json`, verify auth with `paperclipai auth whoami --json`, confirm the route with a safe GET where possible, write one dependency at a time, read back native fields, and never print bearer tokens.

## Boundaries

- Paperclip-only mutation. Recording the Twenty segment means storing a pointer; creating a Twenty list or saved view is a Twenty write, so route it to `twenty-admin` with its own dry-run and approval.
- Record intent, do not execute. Do not run a stage, set a stage to `running`, assign the run issue, or move it to `todo`.
- One run at a time. Do not bundle multiple runs into one Run Record.
- v1 has no send run. A push-stage Run Record ends at "list created and attached to a campaign"; sending is automatic in the sending tool.
