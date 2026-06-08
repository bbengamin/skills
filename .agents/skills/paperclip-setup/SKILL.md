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

2. If `paperclipai` is missing, guide a fresh install.

   First check whether the environment can install the npm package:

   ```sh
   command -v node
   node --version
   command -v npm
   npm --version
   ```

   If Node.js and npm are present, tell the operator to install the CLI globally:

   ```sh
   npm install -g paperclipai
   ```

   Then verify the binary is on `PATH`:

   ```sh
   command -v paperclipai
   paperclipai --version
   ```

   If install succeeds but `command -v paperclipai` still fails, inspect npm's global binary directory and tell the operator to add it to `PATH`:

   ```sh
   npm bin -g
   ```

   Do not run a global install without operator approval. If Node.js or npm are missing, ask the operator to install Node.js for their platform first, then rerun setup.

3. If the CLI is installed but auth or context is missing, guide login and context selection.

   ```sh
   paperclipai auth login
   paperclipai company list --json
   paperclipai context show --json
   ```

   If no company is selected after login, ask the operator which company to use. Do not guess across companies.

4. Inspect available companies if Paperclip auth is configured.

   ```sh
   paperclipai company list --json
   ```

5. Confirm the active company scope.

   If no company is selected, ask the operator which company to use. Do not guess across companies.

6. Verify shared docs exist.

   Required files:

   - `AGENTS.md`
   - `CONTEXT.md`
   - `docs/paperclip-operator/control-plane.md`
   - `docs/paperclip-operator/workflow.md`
   - `docs/paperclip-operator/afk-readiness.md`
   - `docs/paperclip-operator/cli-contract.md`
   - `docs/paperclip-operator/integration-matrix.md`
   - `docs/paperclip-operator/paperclip-docs-index.md`

7. If docs are missing, propose scaffolding them.

   Show the exact files that will be created or updated. Ask for approval before writing.

   Use bundled templates from `references/project-docs/`. Create missing directories as needed.

   If a target file already exists, do not overwrite it silently. Summarize the conflict and ask whether to skip, merge manually, or replace.

8. Report setup status.

   Include:

   - whether `paperclipai` was found or install guidance was given
   - CLI path and version
   - active profile
   - API base
   - company id, if configured
   - auth state or next auth command needed
   - docs created, docs skipped, or remaining missing docs
   - unresolved setup questions

## Mutation Rule

This skill may read freely. Ask before changing CLI context, creating Paperclip records, installing Paperclip company skills, or editing shared docs. Creating missing shared docs from bundled templates is allowed only after operator approval.
