#!/usr/bin/env python3
"""Materialize self-contained skill references from canonical repository docs."""

from __future__ import annotations

import argparse
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
        data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        if data.get("version") != 1:
            raise ManifestError("skill-references.json must use version 1")

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
        return problems

    def sync(self) -> tuple[int, int]:
        mappings = self.mappings()
        expected = {mapping.destination for mapping in mappings}
        removed = 0
        for extra in sorted(self._owned_destinations() - expected, reverse=True):
            if extra.exists() or extra.is_symlink():
                extra.unlink()
                removed += 1
                self._remove_empty_parents(extra.parent)

        updated = 0
        for mapping in mappings:
            source_bytes = mapping.source.read_bytes()
            if mapping.destination.exists() and mapping.destination.read_bytes() == source_bytes:
                continue
            mapping.destination.parent.mkdir(parents=True, exist_ok=True)
            self._write_bytes_atomic(mapping.destination, source_bytes)
            updated += 1
        self._write_bytes_atomic(
            self.lock_path,
            (json.dumps(self._lock_payload(mappings), indent=2) + "\n").encode("utf-8"),
        )
        return updated, removed

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

    def _owned_destinations(self) -> set[Path]:
        payload = self._read_lock_payload()
        generated = payload.get("generated", []) if isinstance(payload, dict) else []
        if not isinstance(generated, list):
            raise ManifestError("skill-references.lock.json generated must be an array")
        destinations: set[Path] = set()
        for index, entry in enumerate(generated):
            if not isinstance(entry, dict):
                raise ManifestError(f"lock generated[{index}] must be an object")
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
            skill_dir = self._skill_dir(skill_relative.parts[0])
            owned_relative = Path(*skill_relative.parts[2:])
            destinations.add(
                self._destination_path(
                    skill_dir / "references",
                    str(owned_relative),
                    f"lock generated[{index}]",
                )
            )
        return destinations

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

    def _lock_payload(self, mappings: list[ReferenceMapping]) -> dict[str, object]:
        generated = [
            {
                "source": str(mapping.source.relative_to(self.root)),
                "destination": str(mapping.destination.relative_to(self.root)),
            }
            for mapping in sorted(mappings, key=lambda item: str(item.destination))
        ]
        return {"version": 1, "generated": generated}

    def _read_lock_payload(self) -> dict[str, object]:
        if not self.lock_path.exists():
            return {"version": 1, "generated": []}
        data = json.loads(self.lock_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("version") != 1:
            raise ManifestError("skill-references.lock.json must use version 1")
        return data

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
