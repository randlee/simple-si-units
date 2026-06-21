from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from print_help import render_topic_help
from scope_workspace import prepare_boundary_scope


ROOT = Path(__file__).resolve().parent.parent.parent
TOOL_VERSIONS = json.loads((ROOT / "tool-versions.json").read_text(encoding="utf-8"))


class CiBaselineTests(unittest.TestCase):
    def test_ci_help_mentions_strict_gate(self) -> None:
        output = render_topic_help("ci")
        self.assertIn("sc-boundary", output)
        self.assertIn("clippy", output)

    def test_ci_workflow_matrix_covers_all_platforms(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        actions = TOOL_VERSIONS["github_actions"]
        for runner in actions["runner_os"]:
            self.assertIn(runner, workflow)
        pr_branches = ", ".join(f'"{branch}"' if "*" in branch or "/" in branch else branch for branch in actions["pull_request_branches"])
        push_branches = ", ".join(f'"{branch}"' if "*" in branch or "/" in branch else branch for branch in actions["push_branches"])
        self.assertIn(f"branches: [{pr_branches}]", workflow)
        self.assertIn(f"branches: [{push_branches}]", workflow)
        self.assertIn("run: just ci", workflow)
        self.assertIn(f'toolchain: "{actions["rust_toolchain"]}"', workflow)
        self.assertIn(f'python-version: "{actions["python"]}"', workflow)
        self.assertIn(f'dotnet-version: "{actions["dotnet_sdk"]}"', workflow)
        self.assertIn("python -m pip install -r python/requirements-ci.txt", workflow)
        self.assertIn(f'cargo install just --locked --version {actions["just"]}', workflow)
        self.assertIn(f'cargo install sc-lint --locked --version {actions["sc_lint"]}', workflow)
        self.assertIn(f'cargo install sc-lint-boundary --locked --version {actions["sc_lint_boundary"]}', workflow)

    def test_development_workflow_documents_shipped_scope_exclusion(self) -> None:
        doc = (ROOT / "docs" / "development-workflow.md").read_text(encoding="utf-8")
        self.assertIn("synthetic shipped workspace", doc)
        self.assertIn("reference/", doc)
        self.assertIn("units-x-python", doc)
        self.assertIn("UTF-8", doc)
        self.assertIn("LF", doc)
        self.assertIn("paths containing spaces", doc)

    def test_python_ci_requirements_are_exactly_pinned(self) -> None:
        requirements = (ROOT / "python" / "requirements-ci.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(
            [line.strip() for line in requirements if line.strip()],
            TOOL_VERSIONS["python_ci_requirements"],
        )

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
            self.assertTrue((scope_root / "boundaries" / "units-x-python" / "python-surface.toml").exists())
            self.assertTrue((scope_root / "crates" / "units-x-python").exists())
            manifest_text = manifest_bytes.decode("utf-8")
            self.assertIn('members = ["crates/units-x", "crates/units-x-python"]', manifest_text)


if __name__ == "__main__":
    unittest.main()
