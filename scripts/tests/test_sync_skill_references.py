from __future__ import annotations

import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "sync_skill_references.py"
SPEC = importlib.util.spec_from_file_location("sync_skill_references", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ReferenceMaterializerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "docs").mkdir()
        (self.root / "docs" / "shared.md").write_text("canonical\n", encoding="utf-8")
        skill = self.root / ".agents" / "skills" / "example"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: example\ndescription: test\n---\nbody\n", encoding="utf-8")
        self.write_manifest({"example": ["docs/shared.md"]})
        self.materializer = MODULE.ReferenceMaterializer(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_manifest(
        self,
        skills: dict[str, list[str]],
        project_docs: dict = None,
        skill_transitions: dict[str, str | None] = None,
    ) -> None:
        manifest = {
            "version": 1,
            "skills": skills,
            "projectDocs": project_docs or {},
            "skillTransitions": skill_transitions or {},
        }
        (self.root / "skill-references.json").write_text(json.dumps(manifest), encoding="utf-8")

    def test_sync_and_check_detect_drift(self) -> None:
        self.assertEqual(self.materializer.sync(), (1, 0))
        destination = self.root / ".agents" / "skills" / "example" / "references" / "docs" / "shared.md"
        self.assertEqual(destination.read_text(encoding="utf-8"), "canonical\n")
        self.assertEqual(self.materializer.drift(), [])

        destination.write_text("stale\n", encoding="utf-8")
        self.assertEqual(
            self.materializer.drift(),
            ["stale .agents/skills/example/references/docs/shared.md"],
        )

    def test_sync_removes_only_previously_generated_reference(self) -> None:
        (self.root / "CONTEXT.md").write_text("context\n", encoding="utf-8")
        self.write_manifest({"example": ["CONTEXT.md", "docs/shared.md"]})
        context = self.root / ".agents" / "skills" / "example" / "references" / "CONTEXT.md"
        self.assertEqual(self.materializer.sync(), (2, 0))
        self.assertTrue(context.exists())

        self.write_manifest({"example": ["docs/shared.md"]})
        self.assertEqual(self.materializer.sync(), (0, 1))
        self.assertFalse(context.exists())

    def test_sync_retires_reference_after_skill_is_removed(self) -> None:
        self.materializer.sync()
        skill_file = self.root / ".agents" / "skills" / "example" / "SKILL.md"
        skill_file.unlink()
        self.write_manifest({})

        self.assertEqual(self.materializer.sync(), (0, 1))

    def test_sync_refuses_to_delete_modified_formerly_generated_reference(self) -> None:
        self.materializer.sync()
        destination = (
            self.root
            / ".agents"
            / "skills"
            / "example"
            / "references"
            / "docs"
            / "shared.md"
        )
        destination.write_text("skill authored\n", encoding="utf-8")
        self.write_manifest({})

        with self.assertRaisesRegex(MODULE.ManifestError, "refusing to remove modified"):
            self.materializer.sync()
        self.assertEqual(destination.read_text(encoding="utf-8"), "skill authored\n")

    def test_sync_renames_skill_and_removes_reduced_mapping(self) -> None:
        (self.root / "docs" / "removed.md").write_text("removed\n", encoding="utf-8")
        self.write_manifest({"example": ["docs/removed.md", "docs/shared.md"]})
        self.assertEqual(self.materializer.sync(), (2, 0))

        old_skill = self.root / ".agents" / "skills" / "example"
        renamed_skill = self.root / ".agents" / "skills" / "renamed"
        old_skill.rename(renamed_skill)
        (renamed_skill / "SKILL.md").write_text(
            "---\nname: renamed\ndescription: test\n---\nbody\n", encoding="utf-8"
        )
        self.write_manifest(
            {"renamed": ["docs/shared.md"]},
            skill_transitions={"example": "renamed"},
        )

        self.assertEqual(self.materializer.sync(), (0, 1))
        self.assertFalse((renamed_skill / "references" / "docs" / "removed.md").exists())
        self.assertEqual(self.materializer.drift(), [])

    def test_sync_requires_transition_for_ambiguous_remove_and_add(self) -> None:
        self.materializer.sync()
        old_skill = self.root / ".agents" / "skills" / "example"
        renamed_skill = self.root / ".agents" / "skills" / "renamed"
        old_skill.rename(renamed_skill)
        (renamed_skill / "SKILL.md").write_text(
            "---\nname: renamed\ndescription: test\n---\nbody\n", encoding="utf-8"
        )
        self.write_manifest({"renamed": ["docs/shared.md"]})

        with self.assertRaisesRegex(MODULE.ManifestError, "declare skillTransitions"):
            self.materializer.sync()

    def test_sync_allows_explicit_retirement_while_adding_skill(self) -> None:
        self.materializer.sync()
        (self.root / ".agents" / "skills" / "example" / "SKILL.md").unlink()
        added_skill = self.root / ".agents" / "skills" / "added"
        added_skill.mkdir()
        (added_skill / "SKILL.md").write_text(
            "---\nname: added\ndescription: test\n---\nbody\n", encoding="utf-8"
        )
        self.write_manifest(
            {"added": []},
            skill_transitions={"example": None},
        )

        self.assertEqual(self.materializer.sync(), (0, 1))

    def test_sync_rejects_transition_while_source_skill_is_packageable(self) -> None:
        self.materializer.sync()
        old_skill = self.root / ".agents" / "skills" / "example"
        renamed_skill = self.root / ".agents" / "skills" / "renamed"
        shutil.copytree(old_skill, renamed_skill)
        (renamed_skill / "SKILL.md").write_text(
            "---\nname: renamed\ndescription: test\n---\nbody\n", encoding="utf-8"
        )
        self.write_manifest(
            {"renamed": ["docs/shared.md"]},
            skill_transitions={"example": "renamed"},
        )

        with self.assertRaisesRegex(MODULE.ManifestError, "remains packageable"):
            self.materializer.sync()

    def test_cleanup_preflights_every_retired_reference(self) -> None:
        (self.root / "docs" / "a.md").write_text("a\n", encoding="utf-8")
        (self.root / "docs" / "b.md").write_text("b\n", encoding="utf-8")
        self.write_manifest({"example": ["docs/a.md", "docs/b.md"]})
        self.materializer.sync()
        references = self.root / ".agents" / "skills" / "example" / "references" / "docs"
        (references / "a.md").write_text("modified\n", encoding="utf-8")
        self.write_manifest({})

        with self.assertRaisesRegex(MODULE.ManifestError, "refusing to remove modified"):
            self.materializer.sync()
        self.assertTrue((references / "a.md").exists())
        self.assertTrue((references / "b.md").exists())

    def test_write_preflight_happens_before_cleanup(self) -> None:
        (self.root / "docs" / "retired.md").write_text("retired\n", encoding="utf-8")
        self.write_manifest({"example": ["docs/retired.md"]})
        self.materializer.sync()
        retired = (
            self.root
            / ".agents"
            / "skills"
            / "example"
            / "references"
            / "docs"
            / "retired.md"
        )
        lock_before = (self.root / "skill-references.lock.json").read_bytes()

        canonical_parent = self.root / "docs" / "new"
        canonical_parent.mkdir()
        (canonical_parent / "child.md").write_text("new\n", encoding="utf-8")
        blocked_parent = retired.parent / "new"
        blocked_parent.write_text("not a directory\n", encoding="utf-8")
        self.write_manifest({"example": ["docs/new/child.md"]})

        with self.assertRaisesRegex(MODULE.ManifestError, "write parent is not a directory"):
            self.materializer.sync()
        self.assertTrue(retired.exists())
        self.assertEqual(blocked_parent.read_text(encoding="utf-8"), "not a directory\n")
        self.assertEqual((self.root / "skill-references.lock.json").read_bytes(), lock_before)

    def test_commit_failure_rolls_back_writes_and_removals(self) -> None:
        (self.root / "docs" / "retired.md").write_text("retired\n", encoding="utf-8")
        self.write_manifest({"example": ["docs/retired.md", "docs/shared.md"]})
        self.materializer.sync()
        references = self.root / ".agents" / "skills" / "example" / "references" / "docs"
        shared = references / "shared.md"
        retired = references / "retired.md"
        lock_path = self.root / "skill-references.lock.json"
        lock_before = lock_path.read_bytes()

        (self.root / "docs" / "shared.md").write_text("changed\n", encoding="utf-8")
        (self.root / "docs" / "new.md").write_text("new\n", encoding="utf-8")
        self.write_manifest({"example": ["docs/new.md", "docs/shared.md"]})
        original_write = self.materializer._write_bytes_atomic
        write_calls = 0

        def fail_first_lock_write(destination: Path, content: bytes) -> None:
            nonlocal write_calls
            write_calls += 1
            if write_calls == 3:
                raise OSError("simulated lock failure")
            original_write(destination, content)

        with mock.patch.object(
            self.materializer,
            "_write_bytes_atomic",
            side_effect=fail_first_lock_write,
        ):
            with self.assertRaisesRegex(OSError, "simulated lock failure"):
                self.materializer.sync()

        self.assertEqual(shared.read_text(encoding="utf-8"), "canonical\n")
        self.assertTrue(retired.exists())
        self.assertFalse((references / "new.md").exists())
        self.assertEqual(lock_path.read_bytes(), lock_before)

    def test_sync_preserves_skill_specific_reference(self) -> None:
        unique = self.root / ".agents" / "skills" / "example" / "references" / "docs" / "unique.md"
        unique.parent.mkdir(parents=True)
        unique.write_text("skill specific\n", encoding="utf-8")

        self.materializer.sync()

        self.assertEqual(unique.read_text(encoding="utf-8"), "skill specific\n")

    def test_sync_preserves_skill_specific_project_doc(self) -> None:
        unique = (
            self.root
            / ".agents"
            / "skills"
            / "example"
            / "references"
            / "project-docs"
            / "unique.md"
        )
        unique.parent.mkdir(parents=True)
        unique.write_text("skill specific\n", encoding="utf-8")

        self.materializer.sync()

        self.assertEqual(unique.read_text(encoding="utf-8"), "skill specific\n")

    def test_check_reports_missing_declared_reference(self) -> None:
        self.materializer.sync()
        skill_file = self.root / ".agents" / "skills" / "example" / "SKILL.md"
        skill_file.write_text(
            "---\nname: example\ndescription: test\n---\nRead `references/missing.md`.\n",
            encoding="utf-8",
        )

        self.assertEqual(
            self.materializer.drift(),
            ["broken declaration .agents/skills/example/SKILL.md -> references/missing.md"],
        )

    def test_check_reports_missing_markdown_link(self) -> None:
        self.materializer.sync()
        skill_file = self.root / ".agents" / "skills" / "example" / "SKILL.md"
        skill_file.write_text(
            "---\nname: example\ndescription: test\n---\nRead [missing](references/nope.md).\n",
            encoding="utf-8",
        )

        self.assertEqual(
            self.materializer.drift(),
            ["broken declaration .agents/skills/example/SKILL.md -> references/nope.md"],
        )

    def test_rejects_symlinked_canonical_source(self) -> None:
        with tempfile.TemporaryDirectory() as outside_directory:
            outside = Path(outside_directory) / "secret.md"
            outside.write_text("secret\n", encoding="utf-8")
            link = self.root / "docs" / "link.md"
            link.symlink_to(outside)
            self.write_manifest({"example": ["docs/link.md"]})

            with self.assertRaisesRegex(MODULE.ManifestError, "must not contain symlinks"):
                self.materializer.mappings()

    def test_rejects_invalid_skill_slug(self) -> None:
        self.write_manifest({"example/.": ["docs/shared.md"]})

        with self.assertRaisesRegex(MODULE.ManifestError, "invalid skill slug"):
            self.materializer.mappings()

    def test_rejects_frontmatter_name_mismatch(self) -> None:
        skill_file = self.root / ".agents" / "skills" / "example" / "SKILL.md"
        skill_file.write_text(
            "---\nname: other\ndescription: test\n---\nbody\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(MODULE.ManifestError, "frontmatter name mismatch"):
            self.materializer.mappings()

    def test_rejects_lock_destination_through_symlinked_reference_directory(self) -> None:
        self.materializer.sync()
        references = self.root / ".agents" / "skills" / "example" / "references"
        shared = references / "docs" / "shared.md"
        shared.unlink()
        (references / "docs").rmdir()
        outside = self.root / ".agents" / "skills" / "other" / "references"
        outside.mkdir(parents=True)
        (references / "docs").symlink_to(outside, target_is_directory=True)

        with self.assertRaisesRegex(MODULE.ManifestError, "must not contain symlinks"):
            self.materializer.sync()

    def test_check_reports_symlinked_skill_content(self) -> None:
        self.materializer.sync()
        outside = self.root / "outside.txt"
        outside.write_text("secret\n", encoding="utf-8")
        link = (
            self.root
            / ".agents"
            / "skills"
            / "example"
            / "references"
            / "secret.txt"
        )
        link.symlink_to(outside)

        self.assertIn(
            "symlinked skill content .agents/skills/example/references/secret.txt",
            self.materializer.drift(),
        )

    def test_non_object_manifest_returns_controlled_error(self) -> None:
        for payload in ([], None):
            with self.subTest(payload=payload):
                (self.root / "skill-references.json").write_text(
                    json.dumps(payload), encoding="utf-8"
                )
                errors = io.StringIO()
                with redirect_stderr(errors):
                    result = MODULE.main(["--root", str(self.root)])
                self.assertEqual(result, 2)
                self.assertIn("root must be an object", errors.getvalue())

    def test_manifest_rejects_boolean_and_float_versions(self) -> None:
        for version in (True, 1.0):
            with self.subTest(version=version):
                payload = {
                    "version": version,
                    "skills": {},
                    "projectDocs": {},
                    "skillTransitions": {},
                }
                (self.root / "skill-references.json").write_text(
                    json.dumps(payload), encoding="utf-8"
                )
                with self.assertRaisesRegex(MODULE.ManifestError, "must use version 1"):
                    self.materializer.mappings()

    def test_lock_requires_generated_field_and_complete_entries(self) -> None:
        self.materializer.sync()
        lock_path = self.root / "skill-references.lock.json"
        malformed_payloads = [
            {"version": 2},
            {
                "version": 2,
                "generated": [
                    {
                        "destination": ".agents/skills/example/references/docs/shared.md",
                        "sha256": "0" * 64,
                    }
                ],
            },
        ]
        for payload in malformed_payloads:
            with self.subTest(payload=payload):
                lock_path.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(MODULE.ManifestError):
                    self.materializer.sync()

    def test_manifest_rejects_duplicate_transition_keys(self) -> None:
        (self.root / "skill-references.json").write_text(
            '{"version":1,"skills":{},"projectDocs":{},'
            '"skillTransitions":{"old":"new","old":null}}',
            encoding="utf-8",
        )

        with self.assertRaisesRegex(MODULE.ManifestError, "duplicate JSON key: old"):
            self.materializer.mappings()

    def test_lock_rejects_duplicate_keys(self) -> None:
        self.materializer.sync()
        (self.root / "skill-references.lock.json").write_text(
            '{"version":2,"generated":[],"generated":[]}',
            encoding="utf-8",
        )

        with self.assertRaisesRegex(MODULE.ManifestError, "duplicate JSON key: generated"):
            self.materializer.sync()

    def test_lock_rejects_boolean_and_float_versions(self) -> None:
        self.materializer.sync()
        lock_path = self.root / "skill-references.lock.json"
        for version in (True, 1.0, 2.0):
            with self.subTest(version=version):
                lock_path.write_text(
                    json.dumps({"version": version, "generated": []}),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(
                    MODULE.ManifestError, "must use version 1 or 2"
                ):
                    self.materializer.sync()


if __name__ == "__main__":
    unittest.main()
