from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from print_help import render_topic_help
from scope_workspace import prepare_boundary_scope


ROOT = Path(__file__).resolve().parent.parent.parent


class CiBaselineTests(unittest.TestCase):
    def test_ci_help_mentions_strict_gate(self) -> None:
        output = render_topic_help("ci")
        self.assertIn("sc-boundary", output)
        self.assertIn("clippy", output)

    def test_ci_workflow_matrix_covers_all_platforms(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("macos-latest", workflow)
        self.assertIn("windows-latest", workflow)
        self.assertIn('"integration/*"', workflow)
        self.assertIn("run: just ci", workflow)
        self.assertIn("python/requirements-ci.txt", workflow)

    def test_development_workflow_documents_shipped_scope_exclusion(self) -> None:
        doc = (ROOT / "docs" / "development-workflow.md").read_text(encoding="utf-8")
        self.assertIn("synthetic shipped workspace", doc)
        self.assertIn("reference/", doc)
        self.assertIn("UTF-8", doc)
        self.assertIn("LF", doc)
        self.assertIn("paths containing spaces", doc)

    def test_shipped_scope_workspace_excludes_reference_and_uses_utf8_lf(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units x scope ") as tmpdir:
            scope_root = Path(tmpdir) / "scope with spaces"
            prepare_boundary_scope(ROOT, scope_root)
            manifest_bytes = (scope_root / "Cargo.toml").read_bytes()
            self.assertNotIn(b"\r\n", manifest_bytes)
            self.assertFalse((scope_root / "reference").exists())
            self.assertTrue((scope_root / "boundaries" / "planning.toml").exists())
            self.assertTrue((scope_root / "boundaries" / "units-x" / "core-surface.toml").exists())
            self.assertTrue((scope_root / "crates" / "units-x").exists())


if __name__ == "__main__":
    unittest.main()
