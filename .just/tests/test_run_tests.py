from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest import mock

import run_tests


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")


class RunTestsBehaviorTests(unittest.TestCase):
    def test_run_dotnet_falls_back_to_project_build_when_no_test_project_exists(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-run-tests-") as tmpdir:
            repo_root = Path(tmpdir)
            project = repo_root / "dotnet" / "src" / "UnitsX" / "UnitsX.csproj"
            touch(project)

            with mock.patch.object(run_tests, "run_command", return_value=0) as run_command:
                code = run_tests.run_dotnet(repo_root)

            self.assertEqual(code, 0)
            run_command.assert_called_once_with(
                ["dotnet", "build", str(project), "--nologo"],
                repo_root,
            )

    def test_run_dotnet_skips_when_no_dotnet_project_exists(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-run-tests-") as tmpdir:
            repo_root = Path(tmpdir)

            with mock.patch.object(run_tests, "run_command", return_value=0) as run_command:
                code = run_tests.run_dotnet(repo_root)

            self.assertEqual(code, 0)
            run_command.assert_not_called()


if __name__ == "__main__":
    unittest.main()
