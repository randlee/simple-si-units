from __future__ import annotations

import json
import subprocess
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent.parent


class WorkspaceScaffoldTests(unittest.TestCase):
    def test_expected_scaffolds_exist(self) -> None:
        expected = (
            ROOT / "crates" / "units-x" / "Cargo.toml",
            ROOT / "crates" / "units-x" / "src" / "lib.rs",
            ROOT / "crates" / "units-x-python" / "Cargo.toml",
            ROOT / "crates" / "units-x-python" / "src" / "lib.rs",
            ROOT / "python" / "pyproject.toml",
            ROOT / "python" / "requirements-ci.txt",
            ROOT / "python" / "units_x" / "__init__.py",
            ROOT / "python" / "units_x" / "_version.py",
            ROOT / "dotnet" / "Directory.Build.props",
            ROOT / "dotnet" / "src" / "UnitsX" / "UnitsX.csproj",
            ROOT / ".just" / "run_python_package_smoke.py",
            ROOT / "scripts" / "sync_version_files.py",
            ROOT / "boundaries" / "units-x" / "core-surface.toml",
            ROOT / "boundaries" / "units-x-python" / "python-surface.toml",
        )
        for path in expected:
            self.assertTrue(path.exists(), path.as_posix())

    def test_cargo_metadata_includes_units_x(self) -> None:
        completed = subprocess.run(
            ["cargo", "metadata", "--no-deps", "--format-version", "1"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(completed.stdout)
        package_names = {package["name"] for package in payload["packages"]}
        self.assertIn("units-x", package_names)
        self.assertIn("units-x-python", package_names)
        self.assertNotIn("simple-si-units", package_names)
        self.assertNotIn("simple-si-units-core", package_names)
        self.assertNotIn("simple-si-units-macros", package_names)


if __name__ == "__main__":
    unittest.main()
