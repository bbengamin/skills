# CLI Contract

Local operator skills operate Paperclip through `paperclipai`.

## Discovery

Before mutating, inspect the current context:

```sh
paperclipai context show --json
paperclipai company list --json
paperclipai dashboard get -C <company-id> --json
```

Prefer the active CLI profile and context. Respect user-provided `--profile`, `--context`, `--api-base`, `--api-key`, and `-C/--company-id`.

## JSON First

Use `--json` whenever the command supports it. If a command lacks JSON output, parse conservatively and report uncertainty.

Common reads:

```sh
paperclipai company list --json
paperclipai agent list -C <company-id> --json
paperclipai issue list -C <company-id> --json
paperclipai issue get <issue-id-or-identifier> --json
paperclipai approval list -C <company-id> --json
paperclipai activity list -C <company-id> --json
paperclipai skills list -C <company-id> --json
```

Common writes:

```sh
paperclipai issue create -C <company-id> --title "..." --description "..." --status backlog
paperclipai issue update <issue-id> --status todo --comment "..."
paperclipai issue comment <issue-id> --body "..."
```

Use REST only when the CLI does not expose the needed operation, such as writing keyed issue documents or creating goals/projects if no CLI command exists.

## REST Fallback

The Paperclip API is the supported fallback when the CLI lacks a command. Do not silently downgrade the Paperclip model because a CLI subcommand is missing.

Derive connection details from:

```sh
paperclipai context show --json
```

Use:

- `apiBase` or the active profile API base as the server URL.
- `companyId` or the active profile company id as the company scope.
- the configured API key env var, or `PAPERCLIP_API_KEY`, for bearer auth.

If authentication cannot be derived, ask the operator for the missing credential or ask them to run the relevant `paperclipai auth` or context setup command. Do not create lower-quality artifacts just because REST auth is missing.

Common REST operations not fully covered by the CLI:

```text
GET  /api/companies/{companyId}/goals
POST /api/companies/{companyId}/goals
GET  /api/companies/{companyId}/projects
POST /api/companies/{companyId}/projects
PATCH /api/projects/{projectId}
PUT  /api/issues/{issueId}/documents/plan
```

## Approval Boundary

All operator skills must:

1. Inspect current Paperclip state.
2. Present proposed mutations.
3. Wait for operator approval.
4. Apply the approved mutations.
5. Report created/updated records.

Read-only monitoring does not need confirmation.

## Source of Truth

Do not maintain a duplicate local issue ledger. Local files can be drafts, templates, or skill references. Paperclip control-plane state is canonical.
