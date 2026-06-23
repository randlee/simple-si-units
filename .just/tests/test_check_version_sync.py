from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
import textwrap
import unittest

from check_version_sync import root_version
from check_version_sync import validate_dotnet_version
from check_version_sync import validate_python_version
from check_version_sync import workspace_version


ROOT = Path(__file__).resolve().parent.parent.parent


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class VersionSyncSmokeTests(unittest.TestCase):
    def test_root_version_is_first_publish_version(self) -> None:
        self.assertEqual(root_version(), "0.1.0")

    def test_workspace_version_matches_root_version(self) -> None:
        self.assertEqual(workspace_version(), root_version())

    def test_python_version_is_wired(self) -> None:
        self.assertTrue(validate_python_version(root_version()))

    def test_dotnet_version_is_wired(self) -> None:
        self.assertTrue(validate_dotnet_version(root_version()))

    def test_cli_fails_on_python_version_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-version-sync-") as tmpdir:
            repo_root = Path(tmpdir)
            write_file(repo_root / "version.json", json.dumps({"version": "0.1.0"}) + "\n")
            write_file(
                repo_root / "Cargo.toml",
                textwrap.dedent(
                    """
                    [workspace]
                    members = []
                    resolver = "2"

                    [workspace.package]
                    version = "0.1.0"
                    edition = "2021"
                    license = "MPL-2.0"
                    repository = "https://example.invalid/units-x"
                    homepage = "https://example.invalid/units-x"
                    rust-version = "1.85"
                    """
                ).strip()
                + "\n",
            )
            write_file(
                repo_root / "python" / "pyproject.toml",
                textwrap.dedent(
                    """
                    [project]
                    name = "units-x"
                    version = "0.2.0"
                    """
                ).strip()
                + "\n",
            )
            write_file(repo_root / "python" / "units_x" / "_version.py", '__version__ = "0.1.0"\n')

            completed = subprocess.run(
                [sys.executable, str(ROOT / ".just" / "check_version_sync.py"), "--root", str(repo_root)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("python/pyproject.toml project.version", completed.stderr)


if __name__ == "__main__":
    unittest.main()
