---
name: paperclip-skill-authoring
description: Create or review Paperclip company skills with valid SKILL.md structure, YAML frontmatter, concrete workflows, safety boundaries, examples, validation steps, and frontmatter repair guidance. Use when drafting a new Paperclip skill, fixing malformed skill frontmatter, or preparing a skill for Paperclip import.
---

# Paperclip Skill Authoring

Create or repair Paperclip company skills that load cleanly and give agents enough procedural guidance to act safely.

## Required Shape

Every Paperclip skill must be a folder with a `SKILL.md` file at its root. The file must start with YAML frontmatter delimited by `---` and must include at least:

```yaml
---
name: paperclip-skill-slug
description: Create or review Paperclip skills. Use when an operator asks for skill authoring, skill repair, or Paperclip skill import prep.
---
```

Rules:

- Keep `name` identical to the skill folder slug.
- Use lowercase letters, digits, and hyphens in the slug.
- Write `description` as the trigger contract: what the skill does and when to use it.
- Do not create heading-only `SKILL.md` files. Missing frontmatter is invalid.
- Keep the body in Markdown after the closing `---`.

## Minimal Skeleton

Use this as the smallest acceptable starting point for a Paperclip company skill:

```markdown
---
name: example-paperclip-skill
description: Handle a specific Paperclip workflow. Use when the operator asks to inspect, plan, repair, or validate that workflow.
---

# Example Paperclip Skill

Purpose sentence describing the workflow this skill supports.

## Inputs

- Paperclip company, project, issue, agent, approval, or wiki identifiers needed for the workflow.
- Any local files, URLs, credentials, or operator decisions required before action.

## Workflow

1. Inspect the relevant Paperclip and local state.
2. Identify whether the request is read-only or mutating.
3. Ask for explicit approval before mutating Paperclip, external systems, credentials, or files outside the requested scope.
4. Execute the narrowest safe action.
5. Read back or otherwise verify the result.

## Safety Boundaries

- Read freely when credentials and context are already available.
- Ask before creating, updating, deleting, assigning, approving, spending, sending, or attaching anything.
- Stop when required identifiers, permissions, or approval are missing.

## Verification

- Confirm `SKILL.md` starts with valid YAML frontmatter.
- Confirm required Paperclip records or files changed as expected.
- Report remaining uncertainty and any follow-up import or attachment step.
```

## Authoring Workflow

1. Name the skill with a short lowercase slug that matches the folder name.
2. Write the frontmatter before writing any headings.
3. Make the `description` concrete enough to trigger the skill from user requests without reading the body.
4. Define inputs the agent must gather before acting.
5. Write a step-by-step workflow with clear read, approval, mutation, verification, and reporting phases.
6. Add safety boundaries for Paperclip control-plane mutations, external-account changes, spending, secrets, outreach, and destructive actions.
7. Add stop conditions for missing approval, missing credentials, ambiguous scope, unsafe requested actions, or unavailable verification.
8. Include examples only when they teach the expected shape, command pattern, API shape, or decision rule.
9. Validate before publishing or importing into Paperclip.

## Paperclip-Specific Guidance

Include guidance for these sections when relevant:

- **Trigger language:** describe exact request types that should use the skill.
- **Inputs:** list required Paperclip ids, issue identifiers, company context, files, URLs, tokens, or operator decisions.
- **Workflow:** keep phases ordered; inspect before mutate, mutate only after approval, verify after mutation.
- **Safety boundaries:** identify what the skill must not do without explicit approval.
- **Verification:** describe reads, parser checks, command checks, or API readbacks that prove success.
- **Stop conditions:** tell the agent when to stop and ask rather than guessing.
- **Reporting:** require concise output with changed records, links, validation evidence, and unresolved risks.

## Frontmatter Repair

When repairing a malformed `SKILL.md`, preserve the existing body unless the operator also asked for content edits.

Use this repair process:

1. Read the whole file before editing.
2. If the file begins with a Markdown heading or body text, insert frontmatter above it.
3. If frontmatter exists but is incomplete, update only the YAML block unless the body also needs repair.
4. Set `name` to the folder slug unless the operator explicitly requires a different slug and matching folder rename.
5. Write a concise `description` that includes both purpose and trigger language.
6. Preserve headings, examples, workflow steps, and operator-specific content below the closing `---`.
7. Validate that the repaired file starts with `---`, has a closing `---`, and parses as YAML with `name` and `description`.

Example repair:

```markdown
# Old Skill Title

Existing workflow body...
```

becomes:

```markdown
---
name: old-skill-title
description: Handle the existing workflow. Use when the operator asks for this workflow or needs the skill repaired for Paperclip import.
---

# Old Skill Title

Existing workflow body...
```

## Validation Checklist

Before publishing, packaging, importing, or attaching a Paperclip skill:

- `SKILL.md` is present at the skill folder root.
- The first line is exactly `---`.
- A second `---` closes the frontmatter before the Markdown body.
- YAML parses without errors.
- `name` exists, is non-empty, and matches the folder slug.
- `description` exists, is non-empty, and states when to use the skill.
- The body includes concrete instructions beyond a heading.
- Inputs, workflow, safety boundaries, verification, and stop conditions are covered.
- Examples are included when they prevent ambiguity or repeated mistakes.
- Any live Paperclip import, attachment, or control-plane mutation has explicit operator approval.

Use a parser rather than visual inspection when possible. For example:

```sh
python - path/to/skill/SKILL.md <<'PY'
from pathlib import Path
import sys, yaml

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
print("valid")
PY
```

If `yaml` is unavailable, use the repository's existing validation script or a language-native YAML parser already available in the workspace. Do not rely on regex-only validation for final checks.
