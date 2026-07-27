---
name: paperclip-skill-authoring
description: Create, review, or repair Paperclip company skills with valid SKILL.md frontmatter, predictable workflows, explicit safety boundaries, completion criteria, and import-ready validation. Use when drafting a new Paperclip skill, improving an existing skill, fixing malformed frontmatter, or preparing a skill for Paperclip import.
---

# Paperclip Skill Authoring

Create or repair Paperclip company skills that load cleanly and make agent behavior predictable. A good Paperclip skill should tell the agent when it fires, what state to inspect, what it may mutate, what proves each step is complete, and when to stop.

## Required Shape

Every Paperclip skill is a folder with `SKILL.md` at its root. `SKILL.md` must start with YAML frontmatter delimited by `---` and include `name` and `description`.

```yaml
---
name: paperclip-skill-slug
description: Handle a specific Paperclip workflow. Use when the operator asks to inspect, plan, repair, validate, or execute that workflow.
---
```

Rules:

- `name` matches the folder slug exactly.
- Slugs use lowercase letters, digits, and hyphens.
- `description` is the invocation contract: what the skill does plus the distinct request branches that should trigger it.
- The Markdown body starts after the closing `---` and includes executable guidance beyond a heading.

## Authoring Loop

1. **Choose the branch.** Identify whether the skill drafts, reviews, repairs, imports, attaches, or operates something. If several branches share little workflow, split the skill or disclose branch-only reference behind a clearly worded pointer.
2. **Write the invocation contract.** Keep the description concrete and model-facing. Use one trigger per distinct branch; collapse synonyms that name the same branch.
3. **Define inputs.** List the Paperclip company, project, issue, agent, approval, wiki, local file, credential, URL, or operator decision needed before action. Completion criterion: the agent can tell which inputs are present, missing, or intentionally unnecessary.
4. **Write ordered steps.** Each step must end with a checkable completion criterion. Prefer "read back the updated issue and verify field X" over "ensure the update worked".
5. **Set mutation boundaries.** State what can be read freely, what requires approval, and what is forbidden. Paperclip control-plane writes, external-account changes, spending, outreach, secrets, assignment, approval, import, and destructive actions require explicit approval.
6. **Model event-producing mutations.** When a write triggers asynchronous work, name the single dispatch trigger, require all preparation before it, and define the post-trigger phase as read-only observation. State how to detect queued/running success, skipped/failed dispatch, automatic retries, and full quiescence before correction. Assignment-driven execution must not be paired with heartbeat/resume, mentions, comments, or repeated assignment wakes.
7. **Add stop conditions.** Stop on missing approval, missing credentials, ambiguous identity, unsafe scope, unavailable verification, duplicate records, an already queued/running dispatch, or a request outside the skill's branch.
8. **Add only useful examples.** Keep examples when they prevent a likely malformed frontmatter block, unsafe mutation, wrong API shape, duplicate dispatch, or repeated operator mistake. Delete examples that merely restate the prose.
9. **Validate with a parser.** Completion criterion: frontmatter parses, required fields exist, the body is non-empty, the slug matches the folder, and any live Paperclip import or attachment remains unperformed unless approved.

## Information Hierarchy

Keep `SKILL.md` focused on steps every run needs. Put reference behind a pointer when only one branch needs it.

- **Inline steps:** invocation, inputs, workflow, approvals, verification, stop conditions.
- **Inline reference:** short Paperclip rules the agent needs every run.
- **Disclosed reference:** long schemas, object catalogs, API examples, import docs, or domain policies used by only some branches.

Use one source of truth for each rule. Do not repeat the same safety boundary in the description, workflow, checklist, and examples; put it once where the agent needs it most.

## Minimal Skeleton

Use this as the smallest acceptable starting point:

```markdown
---
name: example-paperclip-skill
description: Handle a specific Paperclip workflow. Use when the operator asks to inspect, plan, repair, validate, or execute that workflow.
---

# Example Paperclip Skill

Purpose sentence naming the workflow and the safe operating posture.

## Inputs

- Required Paperclip identifiers, local files, URLs, credentials, or operator decisions.
- Completion criterion: each input is present, missing, or explicitly unnecessary.

## Workflow

1. Inspect the relevant Paperclip and local state.
2. Decide whether the request is read-only or mutating.
3. For mutating work, present the exact planned change and wait for approval.
4. Execute the narrowest approved action.
5. Read back or otherwise verify the result.

## Safety Boundaries

- Read freely when credentials and context are already available.
- Ask before creating, updating, deleting, assigning, approving, spending, sending, importing, attaching, or changing external systems.
- Stop when identifiers, permissions, approval, or verification are missing.

## Verification

- Confirm `SKILL.md` starts with valid YAML frontmatter.
- Confirm required Paperclip records or files changed as expected.
- Report changed records, validation evidence, uncertainty, and follow-up import or attachment steps.
```

## Frontmatter Repair

When repairing malformed `SKILL.md`, preserve the existing body unless the operator also asks for content edits.

1. Read the whole file before editing.
2. If the file begins with a Markdown heading or body text, insert frontmatter above it.
3. If frontmatter exists but is incomplete, update only the YAML block unless the body also needs repair.
4. Set `name` to the folder slug unless the operator explicitly requires a different slug and matching folder rename.
5. Write `description` with purpose plus trigger branches.
6. Preserve useful headings, examples, workflow steps, and operator-specific content below the closing `---`.
7. Validate with a YAML parser.

Example repair:

```markdown
# Old Skill Title

Existing workflow body...
```

becomes:

```markdown
---
name: old-skill-title
description: Handle the existing Paperclip workflow. Use when the operator asks for that workflow or needs the skill repaired for Paperclip import.
---

# Old Skill Title

Existing workflow body...
```

## Review Checklist

Before publishing, packaging, importing, or attaching a Paperclip skill, verify:

- Required shape: root `SKILL.md`, first line `---`, closing `---`, valid YAML, `name`, `description`, non-empty body.
- Invocation: description has distinct trigger branches and no synonym padding.
- Predictability: ordered steps have checkable completion criteria.
- Paperclip safety: reads, approval-gated mutations, forbidden actions, stop conditions, and verification are explicit.
- Information hierarchy: every line is relevant; branch-only reference is disclosed; duplicate rules and no-op prose are removed.
- Import boundary: no live Paperclip import, attachment, control-plane mutation, or external action happens without explicit operator approval.

Use a parser rather than visual inspection when possible:

```sh
python - path/to/skill/SKILL.md <<'PY'
from pathlib import Path
import sys
import yaml

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
if not text.startswith("---\n"):
    raise SystemExit("SKILL.md must start with YAML frontmatter")
try:
    _, raw, body = text.split("---", 2)
except ValueError:
    raise SystemExit("SKILL.md frontmatter must be closed with ---")
data = yaml.safe_load(raw) or {}
for key in ("name", "description"):
    if not isinstance(data.get(key), str) or not data[key].strip():
        raise SystemExit(f"missing required frontmatter field: {key}")
if not body.strip():
    raise SystemExit("SKILL.md body must not be empty")
if path.parent.name != data["name"]:
    raise SystemExit(f"name must match folder slug: {path.parent.name}")
print("valid")
PY
```

If `yaml` is unavailable, use the repository's existing validation script or a language-native YAML parser already available in the workspace. Do not rely on regex-only validation for final checks.
