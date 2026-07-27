#!/usr/bin/env python3
"""Materialize self-contained skill references from canonical repository docs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ReferenceMapping:
    source: Path
    destination: Path


class ManifestError(ValueError):
    pass


class ReferenceMaterializer:
    def __init__(self, root: Path, manifest_path: Path | None = None) -> None:
        self.root = root.resolve()
        self.manifest_path = (manifest_path or self.root / "skill-references.json").resolve()
        self.skills_root = self.root / ".agents" / "skills"

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
        expected = {mapping.destination for mapping in mappings}
        problems: list[str] = []
        for mapping in mappings:
            relative = mapping.destination.relative_to(self.root)
            if not mapping.destination.exists():
                problems.append(f"missing {relative}")
            elif mapping.destination.read_bytes() != mapping.source.read_bytes():
                problems.append(f"stale {relative}")
        for extra in sorted(self._managed_candidates() - expected):
            problems.append(f"unmanaged {extra.relative_to(self.root)}")
        problems.extend(self._missing_declared_references())
        return problems

    def sync(self) -> tuple[int, int]:
        mappings = self.mappings()
        expected = {mapping.destination for mapping in mappings}
        removed = 0
        for extra in sorted(self._managed_candidates() - expected, reverse=True):
            extra.unlink()
            removed += 1
            self._remove_empty_parents(extra.parent)

        updated = 0
        for mapping in mappings:
            source_bytes = mapping.source.read_bytes()
            if mapping.destination.exists() and mapping.destination.read_bytes() == source_bytes:
                continue
            mapping.destination.parent.mkdir(parents=True, exist_ok=True)
            mapping.destination.write_bytes(source_bytes)
            updated += 1
        return updated, removed

    def _skill_dir(self, skill_name: object) -> Path:
        if not isinstance(skill_name, str) or not skill_name:
            raise ManifestError("skill names must be non-empty strings")
        skill_dir = self.skills_root / skill_name
        if not (skill_dir / "SKILL.md").is_file():
            raise ManifestError(f"skill does not exist: {skill_name}")
        return skill_dir

    def _source_path(self, value: object) -> Path:
        relative = self._safe_relative(value, "source")
        source = self.root / relative
        if not source.is_file():
            raise ManifestError(f"source does not exist: {relative}")
        return source

    def _destination_path(self, base: Path, value: object, field: str) -> Path:
        relative = self._safe_relative(value, field)
        destination = (base / relative).resolve()
        if not destination.is_relative_to(base.resolve()):
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

    def _managed_candidates(self) -> set[Path]:
        candidates: set[Path] = set()
        if not self.skills_root.exists():
            return candidates
        for skill_dir in self.skills_root.iterdir():
            references = skill_dir / "references"
            if not references.is_dir():
                continue
            context = references / "CONTEXT.md"
            if context.is_file():
                candidates.add(context.resolve())
            docs = references / "docs"
            if docs.is_dir():
                for path in docs.rglob("*"):
                    if not path.is_file():
                        continue
                    source = self.root / path.relative_to(references)
                    if source.is_file():
                        candidates.add(path.resolve())
            project_docs = references / "project-docs"
            if project_docs.is_dir():
                candidates.update(path.resolve() for path in project_docs.rglob("*") if path.is_file())
        return candidates

    def _missing_declared_references(self) -> list[str]:
        problems: list[str] = []
        pattern = re.compile(r"`(references/[^`]+)`")
        for skill_file in sorted(self.skills_root.glob("*/SKILL.md")):
            skill_dir = skill_file.parent
            for relative in pattern.findall(skill_file.read_text(encoding="utf-8")):
                target = skill_dir / relative
                if not target.exists():
                    problems.append(
                        f"broken declaration {skill_file.relative_to(self.root)} -> {relative}"
                    )
        return problems

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
