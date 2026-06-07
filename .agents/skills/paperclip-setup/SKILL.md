---
name: paperclip-setup
description: Configure local operator assumptions for working with Paperclip through paperclipai. Use when setting up this repo, checking Paperclip CLI context, or preparing the Paperclip operator skill suite.
---

# Paperclip Setup

Prepare the local operator environment for the Paperclip skill suite.

## References

Read these first:

- `../../../CONTEXT.md`
- `../../../docs/paperclip-operator/control-plane.md`
- `../../../docs/paperclip-operator/workflow.md`
- `../../../docs/paperclip-operator/cli-contract.md`

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
   - `docs/paperclip-operator/paperclip-docs-index.md`

5. Report setup status.

   Include:

   - CLI path and version
   - active profile
   - API base
   - company id, if configured
   - missing docs or unresolved setup questions

## Mutation Rule

This skill may read freely. Ask before changing CLI context, creating Paperclip records, installing Paperclip company skills, or editing shared docs.
