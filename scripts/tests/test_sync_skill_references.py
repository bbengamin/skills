from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path


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

    def write_manifest(self, skills: dict[str, list[str]], project_docs: dict = None) -> None:
        manifest = {
            "version": 1,
            "skills": skills,
            "projectDocs": project_docs or {},
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


if __name__ == "__main__":
    unittest.main()
