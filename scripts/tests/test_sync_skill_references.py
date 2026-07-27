from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
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
        manifest = {
            "version": 1,
            "skills": {"example": ["docs/shared.md"]},
            "projectDocs": {},
        }
        (self.root / "skill-references.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.materializer = MODULE.ReferenceMaterializer(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

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

    def test_sync_removes_unmanaged_shared_reference(self) -> None:
        extra = self.root / ".agents" / "skills" / "example" / "references" / "CONTEXT.md"
        extra.parent.mkdir(parents=True)
        extra.write_text("old\n", encoding="utf-8")

        self.assertEqual(self.materializer.sync(), (1, 1))
        self.assertFalse(extra.exists())

    def test_sync_preserves_skill_specific_reference(self) -> None:
        unique = self.root / ".agents" / "skills" / "example" / "references" / "docs" / "unique.md"
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


if __name__ == "__main__":
    unittest.main()
