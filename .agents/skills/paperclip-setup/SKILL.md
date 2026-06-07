---
name: paperclip-setup
description: Configure local operator assumptions for working with Paperclip through paperclipai. Use when setting up this repo, checking Paperclip CLI context, or preparing the Paperclip operator skill suite.
---

# Paperclip Setup

Prepare the local operator environment for the Paperclip skill suite.

## References

Read these first:

- Project docs if they already exist:
  - `../../../CONTEXT.md`
  - `../../../docs/paperclip-operator/control-plane.md`
  - `../../../docs/paperclip-operator/workflow.md`
  - `../../../docs/paperclip-operator/cli-contract.md`
  - `../../../docs/paperclip-operator/integration-matrix.md`
- Bundled templates when project docs are missing:
  - `references/project-docs/AGENTS.md`
  - `references/project-docs/CONTEXT.md`
  - `references/project-docs/docs/paperclip-operator/control-plane.md`
  - `references/project-docs/docs/paperclip-operator/workflow.md`
  - `references/project-docs/docs/paperclip-operator/afk-readiness.md`
  - `references/project-docs/docs/paperclip-operator/cli-contract.md`
  - `references/project-docs/docs/paperclip-operator/integration-matrix.md`
  - `references/project-docs/docs/paperclip-operator/paperclip-docs-index.md`

## Workflow

1. Inspect the local Paperclip CLI.

   ```sh
   command -v paperclipai
   paperclipai --version
   paperclipai context show --json
   ```

2. Inspect available companies if Paperclip auth is configured.

   ```sh
   paperclipai company list --json
   ```

3. Confirm the active company scope.

   If no company is selected, ask the operator which company to use. Do not guess across companies.

4. Verify shared docs exist.

   Required files:

   - `AGENTS.md`
   - `CONTEXT.md`
   - `docs/paperclip-operator/control-plane.md`
   - `docs/paperclip-operator/workflow.md`
   - `docs/paperclip-operator/afk-readiness.md`
   - `docs/paperclip-operator/cli-contract.md`
   - `docs/paperclip-operator/integration-matrix.md`
   - `docs/paperclip-operator/paperclip-docs-index.md`

5. If docs are missing, propose scaffolding them.

   Show the exact files that will be created or updated. Ask for approval before writing.

   Use bundled templates from `references/project-docs/`. Create missing directories as needed.

   If a target file already exists, do not overwrite it silently. Summarize the conflict and ask whether to skip, merge manually, or replace.

6. Report setup status.

   Include:

   - CLI path and version
   - active profile
   - API base
   - company id, if configured
   - docs created, docs skipped, or remaining missing docs
   - unresolved setup questions

## Mutation Rule

This skill may read freely. Ask before changing CLI context, creating Paperclip records, installing Paperclip company skills, or editing shared docs. Creating missing shared docs from bundled templates is allowed only after operator approval.
