from __future__ import annotations

from pathlib import Path
import unittest

from print_help import render_topic_help


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
        self.assertIn("run: just ci", workflow)

    def test_development_workflow_documents_shipped_scope_exclusion(self) -> None:
        doc = (ROOT / "docs" / "development-workflow.md").read_text(encoding="utf-8")
        self.assertIn("synthetic shipped workspace", doc)
        self.assertIn("reference/", doc)


if __name__ == "__main__":
    unittest.main()
