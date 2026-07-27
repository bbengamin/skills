# Paperclip Operator Skills

Local operator skills for preparing and operating AFK work in Paperclip through the `paperclipai` CLI.

These skills help a human operator turn fuzzy intent into Paperclip-native goals, projects, parent issues, plans, child issues, triage decisions, and monitoring reports while keeping Paperclip as the source of truth.

The repo also includes a `.claude-plugin/plugin.json` manifest so Claude Code can
discover the tracked skills when installing from the GitHub repository.

## Install

List available skills:

```sh
npx skills add bbengamin/skills --list
```

Install all Paperclip operator skills for Claude Code and Codex in the current
project:

```sh
npx skills add bbengamin/skills --skill '*' --agent claude-code codex -y
```

When running from inside an agent, the installer may auto-detect that agent and skip
the interactive client picker. Passing `--agent claude-code codex` keeps the
install scoped to the two supported local clients this suite is usually used with.

Only use `--all` if you intentionally want every skill installed into every
supported agent target:

```sh
npx skills add bbengamin/skills --all
```

The `claude-code` target writes Claude-compatible project skills under:

```text
.claude/skills/
```

The `codex` and universal-agent targets write Codex-compatible project skills under:

```text
.agents/skills/
```

If a project was already installed for Codex only, reinstall into Claude Code:

```sh
npx skills add bbengamin/skills --skill '*' --agent claude-code -y
```

Claude Code also reads project memory from `CLAUDE.md`, not `AGENTS.md`. If
`paperclip-setup` has not scaffolded it yet, create a Claude memory file alongside
`AGENTS.md`:

```sh
cp AGENTS.md CLAUDE.md
```

For Claude/Cowork cloud skill import, each uploaded skill archive must be
self-contained: `SKILL.md` at the archive root, and every referenced file inside
that same skill folder. The tracked skills bundle their shared docs under each
skill's `references/` folder for this reason.

Build one `.skill` upload archive per skill:

```sh
scripts/package-skill-zips.sh
```

Archives are written to `dist/skills/` and are intentionally ignored by git.

Scripts that should ship with a skill live inside that skill's folder (for example the Ralph loop driver at `.agents/skills/outreach-enrich/scripts/ralph-run.sh`), so `npx skills add` installs them with the skill. The repo-root `scripts/` folder holds repo tooling only (packaging) and is not installed.

Install globally:

```sh
npx skills add bbengamin/skills --all -g
```

Install selected skills:

```sh
npx skills add bbengamin/skills --skill paperclip-setup paperclip-clarify paperclip-record-strategy
```

After installing in a fresh project, run `paperclip-setup`. It checks your `paperclipai` context and can scaffold the shared operator docs into the project after you approve:

```text
AGENTS.md
CLAUDE.md
CONTEXT.md
docs/paperclip-operator/
```

## Skill Catalog

### Paperclip Operator

- `paperclip-setup` — check local `paperclipai` context and shared operator docs.
- `paperclip-mvp-grill` — turn a committed product idea into an evidence-aware GTM dossier and approved Paperclip validation plan.
- `paperclip-clarify` — run a non-mutating clarification session.
- `paperclip-record-strategy` — create or select the Paperclip planning chain: Goal, Project, Parent Issue, and `plan` document.
- `paperclip-source-capture` — capture a creator's raw brain-dump into their LLM Wiki space (no-task) and run guided ingest into structured, durable pages for reuse via wiki-ask.
- `paperclip-plan-work` — decompose a strategy artifact or parent issue into one level of child issues.
- `paperclip-triage` — review issues for AFK readiness before delegation.
- `paperclip-monitor` — inspect active execution across agents, heartbeats, activity, approvals, costs, and blocked work.
- `paperclip-admin` — handle ad hoc Paperclip reads, minor approved mutations, existing-agent admin, and company skill-library maintenance.
- `paperclip-create-agent` — create or hire Paperclip agents through the governance-aware native workflow.
- `paperclip-skill-authoring` — create or review Paperclip company skills with valid `SKILL.md` frontmatter, workflow guidance, validation, and repair steps.
- `paperclip-wiki-fetch` — fetch llm-wiki page content, page lists, and captured sources through the plugin bridge API.
- `paperclip-wiki-manage` — create, update, rename, archive, or delete llm-wiki content through confirmed plugin bridge write routes with strict approval and verification.

### Growth Operator

- `growth-clarify` — run a non-mutating clarification session for shared acquisition strategy across inbound and outbound.
- `growth-record-strategy` — record approved growth strategy into goals, durable channel/motion projects, strategy parent issues, branch parent issues, and plan documents.
- `inbound-plan-work` — decompose a growth strategy or inbound branch into one level of backlog inbound/channel work.
- `outbound-plan-work` — decompose a growth strategy or outbound branch into one level of backlog outbound work.
- `inbound-triage` — review planned inbound/channel work for level-aware AFK readiness before delegation.
- `outbound-triage` — review planned outbound work for level-aware AFK readiness across asset prep, tool work, sending, and reply/booking support.

### Outreach Operator

Operator-driven outbound-engine pipeline. Paperclip owns the run intent (the Run Record); Twenty owns the lead data. Per-person work delegates to the shared engine skills.

- `outreach-clarify` — pin the config of one concrete run (campaign, ICP filters, stage scope, tools, caps, QA gates). Non-mutating.
- `outreach-record-run` — materialize the approved run spec into a Paperclip Run Record and initialize its checkpoint.
- `outreach-source` — filtered sourcing (Apollo via composio, or import) into idempotent Twenty ingest.
- `outreach-resolve` — identity match and golden-record merge over the sourced segment, with fuzzy-match human QA.
- `outreach-enrich` — per-lead Ralph worker: one lead per run through a cheapest-first provider waterfall.
- `outreach-gate` — apply the per-person eligibility verdict and dedup, TTL, suppression, and routing.
- `outreach-assemble` — build the omnichannel segment and grounded personalization assets.
- `outreach-push` — create the list in the wired sending tool (Instantly/Grinfi) and attach it to a campaign; activation is operator-gated.
- `outreach-review` — pull reply and campaign signal, capture outcomes, and write the kill/continue signal back to Paperclip.

### Outbound Engine (shared, model-invoked)

- `twenty-engine-sync` — the shared read/write authority for Twenty: identity, idempotent match-or-create, golden-record merge, fuzzy-QA handoff, suppression/routing. Additive, dry-run first.
- `eligibility-gate` — the shared deterministic per-person verdict (reuse / re-enrich / source / suppress / skip) and routing. Decision-only.

## Workflow

```text
clarify -> record strategy -> plan work -> triage -> monitor -> recursive planning
```

Growth strategy branches after the shared strategy is recorded:

```text
growth-clarify -> growth-record-strategy -> inbound-plan-work / outbound-plan-work -> inbound-triage / outbound-triage
```

The outbound-engine run pipeline continues after outbound triage:

```text
outreach-clarify -> outreach-record-run -> [ source -> resolve -> enrich -> gate -> assemble -> push ] -> outreach-review
```

The suite is designed around Paperclip's native hierarchy:

```text
Company -> Goal -> Project -> Issue -> Workspace -> Agent run
```

## Shared References

- `AGENTS.md` — repo-level operating rules.
- `CONTEXT.md` — glossary.
- `docs/paperclip-operator/control-plane.md` — Paperclip entities and lifecycle.
- `docs/paperclip-operator/workflow.md` — skill workflow.
- `docs/paperclip-operator/afk-readiness.md` — readiness rules for AFK issues.
- `docs/paperclip-operator/cli-contract.md` — `paperclipai` usage contract.
- `docs/paperclip-operator/integration-matrix.md` — MCP/CLI/REST operation matrix.
- `docs/paperclip-operator/paperclip-docs-index.md` — upstream Paperclip docs index.
- `docs/growth-operator/control-plane.md` — acquisition goals, durable channel/motion projects, and branch strategy model.
- `docs/growth-operator/workflow.md` — Growth skill workflow.
- `docs/growth-operator/afk-readiness.md` — shared readiness rules for inbound and outbound planning.

These docs are bundled inside `paperclip-setup` as templates so they can be copied into fresh projects.

## Security Scan Notes

These skills are scanned on skills.sh. Two recurring findings are known and accepted:

- **Socket alert on `paperclip-setup`** — flags `npm install -g paperclipai`. This is
  the official first-party Paperclip CLI; the alert is expected for any global package
  install and is not a vulnerability.
- **Generative "critical" ratings on mutation/admin skills** — these skills create
  agents, mutate Paperclip control-plane state, and delegate autonomous work by design.
  Mutations are gated behind explicit operator approval (see the Principles below). The
  non-mutating clarifier skills (`growth-clarify`, `paperclip-clarify`) rate as safe.

No live secrets or internal hostnames ship in the skills; API examples use placeholders.

## Principles

- Paperclip is the source of truth.
- Operator skills inspect before mutating.
- Mutations require operator approval.
- `backlog` means not ready or parked.
- `todo` means ready and actionable.
- Plan one child-issue level at a time.
- Use `blockedByIssueIds` for real dependencies.
- Use goals and sub-goals for durable acquisition direction.
- Use one project per durable inbound channel or outbound motion.
- Use parent issues and plan documents for strategy periods, campaigns, experiments, and branch planning.
- Keep outbound triage level-aware: asset preparation, tool work, sending, and reply/booking support have different approval and stop-condition requirements.
