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
    def test_run_python_invokes_helper_tests_and_native_smoke(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-run-tests-") as tmpdir:
            repo_root = Path(tmpdir)

            with mock.patch.object(run_tests, "run_command", return_value=0) as run_command:
                code = run_tests.run_python(repo_root)

            self.assertEqual(code, 0)
            self.assertEqual(
                [call.args[0][-1] for call in run_command.call_args_list],
                [
                    str(repo_root / ".just/run_pytests.py"),
                    str(repo_root / ".just/run_python_package_smoke.py"),
                ],
            )

    def test_run_all_keeps_native_smoke_in_full_repo_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-run-tests-") as tmpdir:
            repo_root = Path(tmpdir)
            touch(repo_root / "dotnet" / "src" / "UnitsX" / "UnitsX.csproj")

            with mock.patch.object(run_tests, "run_command", return_value=0) as run_command:
                code = run_tests.run_all(repo_root)

            self.assertEqual(code, 0)
            commands = [call.args[0] for call in run_command.call_args_list]
            self.assertIn(
                [run_tests.sys.executable or "python3", str(repo_root / ".just/run_python_package_smoke.py")],
                commands,
            )
            self.assertIn(
                ["cargo", "test", "--manifest-path", str(repo_root / "reference" / "simple-si-units" / "Cargo.toml"), "--all-features"],
                commands,
            )

    def test_run_rust_includes_reference_crate_tests(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-run-tests-") as tmpdir:
            repo_root = Path(tmpdir)

            with mock.patch.object(run_tests, "run_command", return_value=0) as run_command:
                code = run_tests.run_rust(repo_root)

            self.assertEqual(code, 0)
            commands = [call.args[0] for call in run_command.call_args_list]
            self.assertEqual(commands[0], ["cargo", "test", "--workspace", "--all-features"])
            self.assertIn(
                ["cargo", "test", "--manifest-path", str(repo_root / "reference" / "simple-si-units-core" / "Cargo.toml")],
                commands,
            )
            self.assertIn(
                ["cargo", "test", "--manifest-path", str(repo_root / "reference" / "simple-si-units-macros" / "Cargo.toml")],
                commands,
            )
            self.assertIn(
                ["cargo", "test", "--manifest-path", str(repo_root / "reference" / "simple-si-units" / "Cargo.toml"), "--all-features"],
                commands,
            )

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
