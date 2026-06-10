---
name: paperclip-setup
description: Configure local operator assumptions for working with Paperclip through paperclipai and Paperclip MCP fallback. Use when setting up this repo, checking Paperclip CLI context, installing project-local or explicitly global MCP config, or preparing the Paperclip operator skill suite.
---

# Paperclip Setup

Prepare the local operator environment for the Paperclip skill suite.

## References

Read these first:

- Packaged shared docs:
  - `references/CONTEXT.md`
  - `references/docs/paperclip-operator/control-plane.md`
  - `references/docs/paperclip-operator/workflow.md`
  - `references/docs/paperclip-operator/cli-contract.md`
  - `references/docs/paperclip-operator/integration-matrix.md`
- Bundled templates when project docs are missing:
  - `references/project-docs/AGENTS.md`
  - `references/project-docs/CLAUDE.md`
  - `references/project-docs/CONTEXT.md`
  - `references/project-docs/docs/paperclip-operator/control-plane.md`
  - `references/project-docs/docs/paperclip-operator/workflow.md`
  - `references/project-docs/docs/paperclip-operator/afk-readiness.md`
  - `references/project-docs/docs/paperclip-operator/cli-contract.md`
  - `references/project-docs/docs/paperclip-operator/integration-matrix.md`
  - `references/project-docs/docs/paperclip-operator/paperclip-docs-index.md`
  - `references/project-docs/docs/creator-operator/workflow.md`
  - `references/project-docs/docs/creator-operator/control-plane.md`
  - `references/project-docs/docs/creator-operator/afk-readiness.md`
  - `references/project-docs/docs/growth-operator/workflow.md`
  - `references/project-docs/docs/growth-operator/control-plane.md`
  - `references/project-docs/docs/growth-operator/afk-readiness.md`
  - `references/project-docs/docs/growth-operator/tooling-scout.md`

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

3. If the CLI is installed, continue setup instead of stopping at the first failing Paperclip command.

   Treat setup as a ladder:

   - CLI installed and on `PATH`
   - CLI can read its context
   - API base is reachable
   - auth is configured
   - company context is selected
   - Paperclip MCP config is installed or intentionally skipped
   - shared operator docs exist

   A failure at one rung should produce the next concrete command or decision needed, not a generic blocker report.

4. Verify the configured API base before trying company reads.

   Inspect the active context:

   ```sh
   paperclipai context show --json
   ```

   If the API base is missing, empty, or only the unreachable default, ask the operator for the Paperclip environment URL before attempting auth or company commands. Phrase this as a setup input, for example:

   ```text
   What Paperclip environment URL should this CLI use? For example: https://paperclip.example.com or http://localhost:3100.
   ```

   When the operator provides a URL, verify it before writing context:

   ```sh
   curl -fsS <api-base>/api/health
   ```

   If it is reachable, show the proposed context mutation and ask for approval. Before any `context set`, read the current context so existing values can be preserved:

   ```sh
   paperclipai context show --json
   ```

   ```sh
   paperclipai context set --api-base <api-base> --use
   ```

   If the operator wants an isolated or named profile, include `--profile <name>` before `--use`. Treat `context set` as replacing the profile's configured values rather than merging unknown existing fields: when both API base and company id are known, set them together in one command.

   If the API base is `http://localhost:3100`, verify the local Paperclip API is actually running:

   ```sh
   curl -fsS http://localhost:3100/api/health
   ```

   If the API health check fails, report that install is complete but the Paperclip API server is not reachable. Ask whether the operator wants to start the local Paperclip API or provide a different Paperclip environment URL. Do not treat this as an auth failure until the API is reachable.

5. If the API is reachable but auth or context is missing, guide login and context selection.

   ```sh
   paperclipai auth login --api-base <api-base>
   paperclipai company list --json
   paperclipai context show --json
   ```

   If no company is selected after login, ask the operator which company to use. Do not guess across companies.

6. Inspect available companies if Paperclip auth is configured.

   ```sh
   paperclipai company list --json
   ```

7. Confirm the active company scope.

   If no company is selected, ask the operator which company to use. Do not guess across companies.

   When the operator selects a company, preserve the API base while writing the company id:

   ```sh
   paperclipai context set --api-base <api-base> --company-id <company-id> --use
   paperclipai context show --json
   ```

   Verify the resulting profile contains both `apiBase` and `companyId`. If it does not, repair by setting both values together and read the context back again.

8. Verify Paperclip MCP config.

   Paperclip MCP uses `@bbengamin/paperclip-mcp-server` as a fallback surface after CLI. Default to project-local Codex configuration in the current trusted project:

   ```text
   .codex/config.toml
   ```

   Use global Codex configuration only when the operator explicitly asks for global install:

   ```text
   ~/.codex/config.toml
   ```

   Inspect the intended target before proposing a change:

   ```sh
   test -f .codex/config.toml && sed -n '1,220p' .codex/config.toml
   test -f ~/.codex/config.toml && sed -n '1,220p' ~/.codex/config.toml
   ```

   Proposed project-local TOML:

   ```toml
   [mcp_servers.paperclip]
   command = "npx"
   args = ["-y", "@bbengamin/paperclip-mcp-server"]
   ```

   If the operator wants explicit host-local overrides, include only the requested environment values:

   ```toml
   [mcp_servers.paperclip.env]
   PAPERCLIP_API_URL = "<api-base>"
   PAPERCLIP_COMPANY_ID = "<company-id>"
   ```

   Prefer token-free configuration that falls back to the active `paperclipai` profile and board auth. Do not write `PAPERCLIP_API_KEY` into project-local config. If a bearer token is required, ask the operator to use a local environment variable or user-level config.

   Before writing MCP config, show:

   - target scope: project-local or global
   - target path
   - exact TOML table
   - whether the `mcp_servers.paperclip` entry will be created, replaced, or left unchanged

   Ask for explicit approval before editing the config file. After writing, verify:

   ```sh
   sed -n '1,220p' <target-config-path>
   npm view @bbengamin/paperclip-mcp-server version
   ```

   Then tell the operator to restart Codex or start a new thread before expecting Paperclip MCP tools to appear. Do not treat missing MCP tools in the same running thread as install failure unless a restarted session still cannot load them.

9. Verify shared docs exist.

   Required files:

   - `AGENTS.md`
   - `CLAUDE.md`
   - `CONTEXT.md`
   - `docs/paperclip-operator/control-plane.md`
   - `docs/paperclip-operator/workflow.md`
   - `docs/paperclip-operator/afk-readiness.md`
   - `docs/paperclip-operator/cli-contract.md`
   - `docs/paperclip-operator/integration-matrix.md`
   - `docs/paperclip-operator/paperclip-docs-index.md`
   - `docs/creator-operator/workflow.md`
   - `docs/creator-operator/control-plane.md`
   - `docs/creator-operator/afk-readiness.md`
   - `docs/growth-operator/workflow.md`
   - `docs/growth-operator/control-plane.md`
   - `docs/growth-operator/afk-readiness.md`
   - `docs/growth-operator/tooling-scout.md`

10. If docs are missing, propose scaffolding them.

   Show the exact files that will be created or updated. Ask for approval before writing.

   Use bundled templates from `references/project-docs/`. Create missing directories as needed.

   If a target file already exists, do not overwrite it silently. Summarize the conflict and ask whether to skip, merge manually, or replace.

11. Report setup status.

   Include:

   - whether `paperclipai` was found or install guidance was given
   - CLI path and version
   - active profile
   - API base
   - API reachability and whether the next action is starting the local API or changing API base
   - company id, if configured
   - auth state or next auth command needed
   - MCP install scope, target path, and whether restart/new thread is needed
   - docs created, docs skipped, or remaining missing docs
   - unresolved setup questions

## Mutation Rule

This skill may read freely. Ask before changing CLI context, creating Paperclip records, installing or changing Paperclip MCP config, installing Paperclip company skills, or editing shared docs. Creating missing shared docs from bundled templates is allowed only after operator approval.
