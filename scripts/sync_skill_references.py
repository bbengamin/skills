#!/usr/bin/env python3
"""Materialize self-contained skill references from canonical repository docs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class ReferenceMapping:
    source: Path
    destination: Path


@dataclass(frozen=True)
class PlannedWrite:
    destination: Path
    content: bytes


@dataclass(frozen=True)
class FileSnapshot:
    path: Path
    existed: bool
    content: bytes = b""
    mode: int = 0o644


class ManifestError(ValueError):
    pass


class ReferenceMaterializer:
    SKILL_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
    CODE_REFERENCE = re.compile(r"`(references/[^`]+)`")
    MARKDOWN_REFERENCE = re.compile(r"!?\[[^\]]*\]\((references/[^)\s]+)(?:\s+[^)]*)?\)")

    def __init__(self, root: Path, manifest_path: Optional[Path] = None) -> None:
        self.root = root.resolve()
        self.manifest_path = (manifest_path or self.root / "skill-references.json").resolve()
        self.skills_root = self.root / ".agents" / "skills"
        self.lock_path = self.root / "skill-references.lock.json"

    def mappings(self) -> list[ReferenceMapping]:
        data = self._manifest_data()

        mappings: list[ReferenceMapping] = []
        skills = data.get("skills")
        if not isinstance(skills, dict):
            raise ManifestError("skills must be an object")

        for skill_name, sources in sorted(skills.items()):
            skill_dir = self._skill_dir(skill_name)
            if not isinstance(sources, list):
                raise ManifestError(f"skills.{skill_name} must be an array")
            for source_value in sources:
                source = self._source_path(source_value)
                destination = self._destination_path(
                    skill_dir / "references", source_value, f"skills.{skill_name}"
                )
                mappings.append(ReferenceMapping(source, destination))

        project_docs = data.get("projectDocs", {})
        if not isinstance(project_docs, dict):
            raise ManifestError("projectDocs must be an object")
        for skill_name, entries in sorted(project_docs.items()):
            skill_dir = self._skill_dir(skill_name)
            if not isinstance(entries, list):
                raise ManifestError(f"projectDocs.{skill_name} must be an array")
            for index, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    raise ManifestError(f"projectDocs.{skill_name}[{index}] must be an object")
                source = self._source_path(entry.get("source"))
                destination = self._destination_path(
                    skill_dir / "references" / "project-docs",
                    entry.get("destination"),
                    f"projectDocs.{skill_name}[{index}]",
                )
                mappings.append(ReferenceMapping(source, destination))

        destinations: set[Path] = set()
        for mapping in mappings:
            if mapping.destination in destinations:
                raise ManifestError(f"duplicate destination: {mapping.destination}")
            destinations.add(mapping.destination)
        return mappings

    def drift(self) -> list[str]:
        mappings = self.mappings()
        self._ownership_state()
        problems: list[str] = []
        for mapping in mappings:
            relative = mapping.destination.relative_to(self.root)
            if not mapping.destination.exists():
                problems.append(f"missing {relative}")
            elif mapping.destination.read_bytes() != mapping.source.read_bytes():
                problems.append(f"stale {relative}")
        if self._lock_payload(mappings) != self._read_lock_payload():
            problems.append(f"stale {self.lock_path.relative_to(self.root)}")
        problems.extend(self._missing_declared_references())
        problems.extend(self._skill_tree_symlinks())
        return problems

    def sync(self) -> tuple[int, int]:
        mappings = self.mappings()
        expected = {mapping.destination for mapping in mappings}
        owned = self._ownership_state()

        removals: list[Path] = []
        for extra in sorted(owned.keys() - expected, reverse=True):
            if extra.is_symlink():
                raise ManifestError(
                    f"refusing to remove symlinked generated reference: {extra.relative_to(self.root)}"
                )
            if not extra.exists():
                continue
            if not extra.is_file():
                raise ManifestError(
                    f"refusing to remove non-file generated reference: {extra.relative_to(self.root)}"
                )
            expected_digest = owned[extra]
            if expected_digest is None:
                raise ManifestError(
                    f"cannot safely remove lock-v1 reference without digest: {extra.relative_to(self.root)}; "
                    "synchronize before removing its manifest entry"
                )
            if self._content_digest(extra.read_bytes()) != expected_digest:
                raise ManifestError(
                    f"refusing to remove modified formerly generated reference: {extra.relative_to(self.root)}"
                )
            removals.append(extra)

        mapping_contents: dict[Path, bytes] = {}
        mapping_writes: list[PlannedWrite] = []
        for mapping in mappings:
            source_bytes = mapping.source.read_bytes()
            mapping_contents[mapping.destination] = source_bytes
            if mapping.destination.exists() and mapping.destination.read_bytes() == source_bytes:
                continue
            mapping_writes.append(PlannedWrite(mapping.destination, source_bytes))

        lock_content = (
            json.dumps(self._lock_payload(mappings, mapping_contents), indent=2) + "\n"
        ).encode("utf-8")
        lock_write = None
        if not self.lock_path.exists() or self.lock_path.read_bytes() != lock_content:
            lock_write = PlannedWrite(self.lock_path, lock_content)

        self._apply_transaction(
            mapping_writes=mapping_writes,
            removals=removals,
            lock_write=lock_write,
        )
        for extra in removals:
            self._remove_empty_parents(extra.parent)
        return len(mapping_writes), len(removals)

    def _ownership_state(self) -> dict[Path, Optional[str]]:
        manifest = self._manifest_data()
        current_skills = self._manifest_skill_names(manifest)
        transitions = self._skill_transitions(manifest, current_skills)
        owned, locked_skills = self._owned_destinations(transitions)
        added_skills = current_skills - locked_skills
        removed_skills = locked_skills - current_skills
        if added_skills:
            missing_transitions = sorted(removed_skills - transitions.keys())
            if missing_transitions:
                raise ManifestError(
                    "ambiguous removed and added skills; declare skillTransitions for: "
                    + ", ".join(missing_transitions)
                )
        return owned

    def _skill_dir(self, skill_name: object) -> Path:
        if not isinstance(skill_name, str) or not self.SKILL_SLUG.fullmatch(skill_name):
            raise ManifestError(f"invalid skill slug: {skill_name}")
        skill_dir = self.skills_root / skill_name
        if skill_dir.is_symlink():
            raise ManifestError(f"skill directory must not be a symlink: {skill_name}")
        resolved = skill_dir.resolve()
        if not resolved.is_relative_to(self.skills_root.resolve()) or resolved.name != skill_name:
            raise ManifestError(f"skill escapes skills directory: {skill_name}")
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file() or skill_file.is_symlink():
            raise ManifestError(f"skill does not exist: {skill_name}")
        frontmatter_name = self._frontmatter_name(skill_file)
        if frontmatter_name != skill_name:
            raise ManifestError(
                f"skill frontmatter name mismatch: {skill_name} != {frontmatter_name}"
            )
        return skill_dir

    def _source_path(self, value: object) -> Path:
        relative = self._safe_relative(value, "source")
        source = self.root / relative
        current = self.root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise ManifestError(f"source must not contain symlinks: {relative}")
        try:
            resolved = source.resolve(strict=True)
        except FileNotFoundError:
            raise ManifestError(f"source does not exist: {relative}")
        if not resolved.is_relative_to(self.root):
            raise ManifestError(f"source escapes repository: {relative}")
        if not resolved.is_file():
            raise ManifestError(f"source is not a file: {relative}")
        return resolved

    def _destination_path(self, base: Path, value: object, field: str) -> Path:
        relative = self._safe_relative(value, field)
        try:
            base_relative = base.relative_to(self.root)
        except ValueError as error:
            raise ManifestError(f"destination base escapes repository: {base}") from error
        current = self.root
        for part in base_relative.parts:
            current = current / part
            if current.is_symlink():
                raise ManifestError(f"destination must not contain symlinks: {value}")
        base = base.resolve()
        destination = base / relative
        current = base
        for part in relative.parts[:-1]:
            current = current / part
            if current.is_symlink():
                raise ManifestError(f"destination must not contain symlinks: {value}")
        if destination.is_symlink():
            raise ManifestError(f"destination must not be a symlink: {value}")
        if not destination.resolve(strict=False).is_relative_to(base):
            raise ManifestError(f"destination escapes references directory: {value}")
        return destination

    @staticmethod
    def _safe_relative(value: object, field: str) -> Path:
        if not isinstance(value, str) or not value:
            raise ManifestError(f"{field} must be a non-empty string")
        relative = Path(value)
        if relative.is_absolute() or ".." in relative.parts:
            raise ManifestError(f"{field} must be a safe relative path: {value}")
        return relative

    def _manifest_data(self) -> dict[str, object]:
        data = self._read_json(self.manifest_path)
        if not isinstance(data, dict):
            raise ManifestError("skill-references.json root must be an object")
        version = data.get("version")
        if type(version) is not int or version != 1:
            raise ManifestError("skill-references.json must use version 1")
        return data

    def _manifest_skill_names(self, data: dict[str, object]) -> set[str]:
        names: set[str] = set()
        for field in ("skills", "projectDocs"):
            value = data.get(field, {})
            if not isinstance(value, dict):
                raise ManifestError(f"{field} must be an object")
            for skill_name in value:
                if not isinstance(skill_name, str) or not self.SKILL_SLUG.fullmatch(skill_name):
                    raise ManifestError(f"invalid skill slug: {skill_name}")
                names.add(skill_name)
        return names

    def _skill_transitions(
        self, data: dict[str, object], current_skills: set[str]
    ) -> dict[str, Optional[str]]:
        raw = data.get("skillTransitions", {})
        if not isinstance(raw, dict):
            raise ManifestError("skillTransitions must be an object")
        transitions: dict[str, Optional[str]] = {}
        for old_skill, new_skill in raw.items():
            if not isinstance(old_skill, str) or not self.SKILL_SLUG.fullmatch(old_skill):
                raise ManifestError(f"invalid transition source skill slug: {old_skill}")
            if old_skill in current_skills:
                raise ManifestError(f"active skill cannot be a transition source: {old_skill}")
            if new_skill is not None and (
                not isinstance(new_skill, str) or not self.SKILL_SLUG.fullmatch(new_skill)
            ):
                raise ManifestError(f"invalid transition target skill slug: {new_skill}")
            if new_skill == old_skill:
                raise ManifestError(f"skill transition cannot target itself: {old_skill}")
            old_skill_file = self.skills_root / old_skill / "SKILL.md"
            if old_skill_file.exists() or old_skill_file.is_symlink():
                raise ManifestError(
                    f"transition source skill remains packageable: {old_skill}"
                )
            transitions[old_skill] = new_skill

        for old_skill in transitions:
            target = self._resolve_skill_transition(old_skill, transitions)
            if target is not None and target not in current_skills:
                raise ManifestError(
                    f"skill transition target must be active: {old_skill} -> {target}"
                )
        return transitions

    @staticmethod
    def _resolve_skill_transition(
        skill_name: str, transitions: dict[str, Optional[str]]
    ) -> Optional[str]:
        current = skill_name
        visited: set[str] = set()
        while current in transitions:
            if current in visited:
                raise ManifestError(f"skill transition cycle includes: {current}")
            visited.add(current)
            target = transitions[current]
            if target is None:
                return None
            current = target
        return current

    def _owned_destinations(
        self, transitions: dict[str, Optional[str]]
    ) -> tuple[dict[Path, Optional[str]], set[str]]:
        payload = self._read_lock_payload()
        version = payload["version"]
        generated = payload["generated"]
        destinations: dict[Path, Optional[str]] = {}
        locked_skills: set[str] = set()
        for index, entry in enumerate(generated):
            if not isinstance(entry, dict):
                raise ManifestError(f"lock generated[{index}] must be an object")
            required_fields = {"source", "destination"}
            if version == 2:
                required_fields.add("sha256")
            if set(entry) != required_fields:
                raise ManifestError(
                    f"lock generated[{index}] fields must be: "
                    + ", ".join(sorted(required_fields))
                )
            self._safe_relative(entry["source"], f"lock generated[{index}].source")
            relative = self._safe_relative(entry.get("destination"), f"lock generated[{index}]")
            destination = self.root / relative
            try:
                skill_relative = destination.relative_to(self.skills_root)
            except ValueError as error:
                raise ManifestError(f"owned destination escapes skills directory: {relative}") from error
            if len(skill_relative.parts) < 3 or skill_relative.parts[1] != "references":
                raise ManifestError(f"owned destination is not a skill reference: {relative}")
            if not self.SKILL_SLUG.fullmatch(skill_relative.parts[0]):
                raise ManifestError(f"owned destination has invalid skill slug: {relative}")
            locked_skill = skill_relative.parts[0]
            locked_skills.add(locked_skill)
            transitioned_skill = self._resolve_skill_transition(locked_skill, transitions)
            effective_skill = transitioned_skill or locked_skill
            owned_relative = Path(*skill_relative.parts[2:])
            destination = self._destination_path(
                self.skills_root / effective_skill / "references",
                str(owned_relative),
                f"lock generated[{index}]",
            )
            digest = entry.get("sha256")
            if version == 2:
                if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                    raise ManifestError(
                        f"lock generated[{index}] sha256 must be a lowercase digest"
                    )
            else:
                digest = None
            if destination in destinations:
                raise ManifestError(f"duplicate owned destination: {relative}")
            destinations[destination] = digest
        return destinations, locked_skills

    def _missing_declared_references(self) -> list[str]:
        problems: list[str] = []
        for skill_file in sorted(self.skills_root.glob("*/SKILL.md")):
            skill_dir = skill_file.parent
            text = skill_file.read_text(encoding="utf-8")
            references = set(self.CODE_REFERENCE.findall(text))
            references.update(self.MARKDOWN_REFERENCE.findall(text))
            for relative in sorted(references):
                path_without_fragment = relative.split("#", 1)[0].split("?", 1)[0]
                try:
                    safe_relative = self._safe_relative(path_without_fragment, "declared reference")
                except ManifestError:
                    problems.append(
                        f"unsafe declaration {skill_file.relative_to(self.root)} -> {relative}"
                    )
                    continue
                target = skill_dir / safe_relative
                if not target.exists():
                    problems.append(
                        f"broken declaration {skill_file.relative_to(self.root)} -> {relative}"
                    )
        return problems

    def _lock_payload(
        self,
        mappings: list[ReferenceMapping],
        contents: Optional[dict[Path, bytes]] = None,
    ) -> dict[str, object]:
        generated = [
            {
                "source": str(mapping.source.relative_to(self.root)),
                "destination": str(mapping.destination.relative_to(self.root)),
                "sha256": self._content_digest(
                    contents[mapping.destination]
                    if contents is not None
                    else mapping.source.read_bytes()
                ),
            }
            for mapping in sorted(mappings, key=lambda item: str(item.destination))
        ]
        return {"version": 2, "generated": generated}

    def _read_lock_payload(self) -> dict[str, object]:
        if self.lock_path.is_symlink():
            raise ManifestError("skill-references.lock.json must not be a symlink")
        if not self.lock_path.exists():
            return {"version": 2, "generated": []}
        data = self._read_json(self.lock_path)
        if not isinstance(data, dict):
            raise ManifestError("skill-references.lock.json must use version 1 or 2")
        version = data.get("version")
        if type(version) is not int or version not in (1, 2):
            raise ManifestError("skill-references.lock.json must use version 1 or 2")
        if set(data) != {"version", "generated"}:
            raise ManifestError("skill-references.lock.json fields must be: generated, version")
        if not isinstance(data["generated"], list):
            raise ManifestError("skill-references.lock.json generated must be an array")
        return data

    def _apply_transaction(
        self,
        mapping_writes: list[PlannedWrite],
        removals: list[Path],
        lock_write: Optional[PlannedWrite],
    ) -> None:
        writes = list(mapping_writes)
        if lock_write is not None:
            writes.append(lock_write)
        self._preflight_writes(writes)

        paths = {write.destination for write in writes}
        paths.update(removals)
        snapshots = {path: self._snapshot(path) for path in paths}
        created_directories: list[Path] = []
        try:
            for directory in self._missing_parent_directories(writes):
                directory.mkdir()
                created_directories.append(directory)
            for write in mapping_writes:
                self._write_bytes_atomic(write.destination, write.content)
            for extra in removals:
                extra.unlink()
            if lock_write is not None:
                self._write_bytes_atomic(lock_write.destination, lock_write.content)
        except OSError as error:
            rollback_errors = self._rollback(snapshots, created_directories)
            if rollback_errors:
                raise ManifestError(
                    f"sync failed and rollback was incomplete: {error}; "
                    + "; ".join(rollback_errors)
                ) from error
            raise

    def _preflight_writes(self, writes: list[PlannedWrite]) -> None:
        destinations = {write.destination for write in writes}
        if len(destinations) != len(writes):
            raise ManifestError("transaction contains duplicate write destinations")
        for destination in sorted(destinations):
            if not destination.is_relative_to(self.root):
                raise ManifestError(f"write destination escapes repository: {destination}")
            if destination.is_symlink():
                raise ManifestError(
                    f"write destination must not be a symlink: {destination.relative_to(self.root)}"
                )
            if destination.exists() and not destination.is_file():
                raise ManifestError(
                    f"write destination is not a file: {destination.relative_to(self.root)}"
                )
            current = destination.parent
            while current != self.root:
                if current in destinations:
                    raise ManifestError(
                        f"write destination is also a parent path: {current.relative_to(self.root)}"
                    )
                if current.exists() and not current.is_dir():
                    raise ManifestError(
                        f"write parent is not a directory: {current.relative_to(self.root)}"
                    )
                if current.is_symlink():
                    raise ManifestError(
                        f"write parent must not be a symlink: {current.relative_to(self.root)}"
                    )
                current = current.parent

    def _missing_parent_directories(self, writes: list[PlannedWrite]) -> list[Path]:
        missing: set[Path] = set()
        for write in writes:
            current = write.destination.parent
            while current != self.root and not current.exists():
                missing.add(current)
                current = current.parent
        return sorted(missing, key=lambda path: len(path.parts))

    @staticmethod
    def _snapshot(path: Path) -> FileSnapshot:
        if not path.exists():
            return FileSnapshot(path=path, existed=False)
        return FileSnapshot(
            path=path,
            existed=True,
            content=path.read_bytes(),
            mode=path.stat().st_mode & 0o777,
        )

    def _rollback(
        self, snapshots: dict[Path, FileSnapshot], created_directories: list[Path]
    ) -> list[str]:
        errors: list[str] = []
        for snapshot in snapshots.values():
            try:
                if snapshot.existed:
                    snapshot.path.parent.mkdir(parents=True, exist_ok=True)
                    self._write_bytes_atomic(snapshot.path, snapshot.content)
                    snapshot.path.chmod(snapshot.mode)
                elif snapshot.path.exists() or snapshot.path.is_symlink():
                    snapshot.path.unlink()
            except OSError as error:
                errors.append(f"restore {snapshot.path}: {error}")
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        return errors

    @staticmethod
    def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ManifestError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def _read_json(self, path: Path) -> object:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=self._reject_duplicate_keys,
        )

    def _skill_tree_symlinks(self) -> list[str]:
        problems: list[str] = []
        if not self.skills_root.exists():
            return problems
        for directory, child_directories, files in os.walk(self.skills_root, followlinks=False):
            parent = Path(directory)
            for name in sorted(child_directories + files):
                candidate = parent / name
                if candidate.is_symlink():
                    problems.append(f"symlinked skill content {candidate.relative_to(self.root)}")
        return problems

    @staticmethod
    def _content_digest(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def _frontmatter_name(skill_file: Path) -> str:
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            raise ManifestError(f"skill frontmatter missing: {skill_file}")
        try:
            _, frontmatter, _ = text.split("---", 2)
        except ValueError as error:
            raise ManifestError(f"skill frontmatter is not closed: {skill_file}") from error
        for line in frontmatter.splitlines():
            if line.startswith("name:"):
                return line.split(":", 1)[1].strip().strip("\"'")
        raise ManifestError(f"skill frontmatter name missing: {skill_file}")

    @staticmethod
    def _write_bytes_atomic(destination: Path, content: bytes) -> None:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
        )
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            mode = destination.stat().st_mode & 0o777 if destination.exists() else 0o644
            temporary.chmod(mode)
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)

    def _remove_empty_parents(self, directory: Path) -> None:
        references_roots = {
            (skill / "references").resolve()
            for skill in self.skills_root.iterdir()
            if (skill / "references").is_dir()
        }
        current = directory.resolve()
        while current not in references_roots and current.is_relative_to(self.skills_root.resolve()):
            try:
                current.rmdir()
            except OSError:
                break
            current = current.parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path, help="override the manifest path")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    materializer = ReferenceMaterializer(args.root, args.manifest)
    try:
        if args.check:
            problems = materializer.drift()
            if problems:
                print("skill reference drift detected:", file=sys.stderr)
                for problem in problems:
                    print(f"- {problem}", file=sys.stderr)
                return 1
            print(f"skill references valid: {len(materializer.mappings())} files")
            return 0
        updated, removed = materializer.sync()
        problems = materializer.drift()
        if problems:
            print("skill reference sync left invalid state:", file=sys.stderr)
            for problem in problems:
                print(f"- {problem}", file=sys.stderr)
            return 1
        print(f"skill references synchronized: {updated} updated, {removed} removed")
        return 0
    except (OSError, json.JSONDecodeError, ManifestError) as error:
        print(f"skill reference error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
