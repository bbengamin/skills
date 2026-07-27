#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_root="$repo_root/.agents/skills"
out_dir="$repo_root/dist/skills"

mkdir -p "$out_dir"

python3 "$repo_root/scripts/sync_skill_references.py" --check

symlink_path="$(find "$skills_root" -type l -print -quit)"
if [[ -n "$symlink_path" ]]; then
  printf 'refusing to package symlinked skill content: %s\n' "$symlink_path" >&2
  exit 1
fi

find "$out_dir" -maxdepth 1 -type f -name '*.skill' -delete

while IFS= read -r skill_dir; do
  skill_name="$(basename "$skill_dir")"
  (
    cd "$skill_dir"
    zip -qr "$out_dir/$skill_name.skill" .
  )
  printf 'wrote %s\n' "$out_dir/$skill_name.skill"
done < <(find "$skills_root" -mindepth 1 -maxdepth 1 -type d -exec test -f '{}/SKILL.md' ';' -print | sort)
