from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import run_tests


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")


def isolated_git_env(repo_root: Path) -> dict[str, str]:
    hooks_dir = repo_root / ".git-hooks-empty"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    global_config = repo_root / ".gitconfig"
    global_config.write_text("", encoding="utf-8")

    env = os.environ.copy()
    env["GIT_CONFIG_GLOBAL"] = str(global_config)
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_TEMPLATE_DIR"] = str(repo_root / ".git-template-empty")
    env["HOME"] = str(repo_root)
    env["XDG_CONFIG_HOME"] = str(repo_root / ".xdg-config")
    env["HUSKY"] = "0"
    return env


def git(
    command: list[str],
    repo_root: Path,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=repo_root, check=True, capture_output=True, text=True, env=env)


class RunTestsBehaviorTests(unittest.TestCase):
    def test_generated_artifact_paths_include_all_generated_rust_outputs(self) -> None:
        self.assertIn("crates/units-x/src/generated/arithmetic_impls.rs", run_tests.GENERATED_ARTIFACT_PATHS)
        self.assertIn("crates/units-x/src/generated/bulk_storage_impls.rs", run_tests.GENERATED_ARTIFACT_PATHS)

    def test_generated_artifacts_are_dirty_detects_staged_changes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-run-tests-") as tmpdir:
            repo_root = Path(tmpdir)
            env = isolated_git_env(repo_root)
            git(["git", "init"], repo_root, env)
            git(["git", "config", "core.hooksPath", str(repo_root / ".git-hooks-empty")], repo_root, env)
            git(["git", "config", "commit.gpgsign", "false"], repo_root, env)
            git(["git", "config", "user.email", "tests@example.invalid"], repo_root, env)
            git(["git", "config", "user.name", "units-x tests"], repo_root, env)
            for relative_path in run_tests.GENERATED_ARTIFACT_PATHS:
                touch(repo_root / relative_path)
            git(["git", "add", "."], repo_root, env)
            git(["git", "commit", "-m", "baseline"], repo_root, env)

            target = repo_root / run_tests.GENERATED_ARTIFACT_PATHS[0]
            target.write_text("changed\n", encoding="utf-8")
            git(["git", "add", str(target.relative_to(repo_root))], repo_root, env)

            self.assertTrue(run_tests.generated_artifacts_are_dirty(repo_root))

    def test_generated_artifacts_are_dirty_detects_untracked_generated_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-run-tests-") as tmpdir:
            repo_root = Path(tmpdir)
            env = isolated_git_env(repo_root)
            git(["git", "init"], repo_root, env)
            git(["git", "config", "core.hooksPath", str(repo_root / ".git-hooks-empty")], repo_root, env)
            git(["git", "config", "commit.gpgsign", "false"], repo_root, env)
            git(["git", "config", "user.email", "tests@example.invalid"], repo_root, env)
            git(["git", "config", "user.name", "units-x tests"], repo_root, env)
            for relative_path in run_tests.GENERATED_ARTIFACT_PATHS[:-1]:
                touch(repo_root / relative_path)
            git(["git", "add", "."], repo_root, env)
            git(["git", "commit", "-m", "baseline"], repo_root, env)

            touch(repo_root / run_tests.GENERATED_ARTIFACT_PATHS[-1])

            self.assertTrue(run_tests.generated_artifacts_are_dirty(repo_root))

    def test_generated_artifacts_are_dirty_detects_new_generated_rust_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-run-tests-") as tmpdir:
            repo_root = Path(tmpdir)
            env = isolated_git_env(repo_root)
            git(["git", "init"], repo_root, env)
            git(["git", "config", "core.hooksPath", str(repo_root / ".git-hooks-empty")], repo_root, env)
            git(["git", "config", "commit.gpgsign", "false"], repo_root, env)
            git(["git", "config", "user.email", "tests@example.invalid"], repo_root, env)
            git(["git", "config", "user.name", "units-x tests"], repo_root, env)
            for relative_path in run_tests.GENERATED_ARTIFACT_PATHS:
                touch(repo_root / relative_path)
            git(["git", "add", "."], repo_root, env)
            git(["git", "commit", "-m", "baseline"], repo_root, env)

            for relative_path in (
                "crates/units-x/src/generated/arithmetic_impls.rs",
                "crates/units-x/src/generated/bulk_storage_impls.rs",
            ):
                target = repo_root / relative_path
                target.write_text("changed\n", encoding="utf-8")
                git(["git", "add", str(target.relative_to(repo_root))], repo_root, env)
                self.assertTrue(run_tests.generated_artifacts_are_dirty(repo_root))
                git(["git", "reset", "HEAD", str(target.relative_to(repo_root))], repo_root, env)
                git(["git", "checkout", "--", str(target.relative_to(repo_root))], repo_root, env)

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

            with mock.patch.object(run_tests, "generated_artifacts_are_dirty", return_value=False), mock.patch.object(
                run_tests, "run_command", return_value=0
            ) as run_command:
                code = run_tests.run_all(repo_root)

            self.assertEqual(code, 0)
            commands = [call.args[0] for call in run_command.call_args_list]
            self.assertIn(
                [run_tests.sys.executable or "python3", str(repo_root / "scripts/sync_tool_versions.py"), "--check"],
                commands,
            )
            self.assertIn(
                [run_tests.sys.executable or "python3", str(repo_root / ".just/run_python_package_smoke.py")],
                commands,
            )
            self.assertIn(
                [run_tests.sys.executable or "python3", str(repo_root / "scripts/check_generated_artifacts_clean.py")],
                commands,
            )
            self.assertIn(
                ["cargo", "test", "--manifest-path", str(repo_root / "reference" / "simple-si-units" / "Cargo.toml"), "--all-features"],
                commands,
            )
            self.assertLess(
                commands.index(["just", "generate"]),
                commands.index(
                    [run_tests.sys.executable or "python3", str(repo_root / "scripts/check_generated_artifacts_clean.py")]
                ),
            )

    def test_run_all_uses_post_generate_catalog_check_when_generated_files_were_already_dirty(self) -> None:
        with tempfile.TemporaryDirectory(prefix="units-x-run-tests-") as tmpdir:
            repo_root = Path(tmpdir)
            touch(repo_root / "dotnet" / "src" / "UnitsX" / "UnitsX.csproj")

            with mock.patch.object(run_tests, "generated_artifacts_are_dirty", return_value=True), mock.patch.object(
                run_tests, "run_command", return_value=0
            ) as run_command:
                code = run_tests.run_all(repo_root)

            self.assertEqual(code, 0)
            commands = [call.args[0] for call in run_command.call_args_list]
            catalog_check = [
                run_tests.sys.executable or "python3",
                str(repo_root / "scripts/generate_catalog_artifacts.py"),
                "--mode",
                "check",
            ]
            self.assertEqual(
                sum(1 for command in commands if command == catalog_check),
                2,
            )
            self.assertLess(commands.index(["just", "generate"]), len(commands) - 1)
            self.assertIn(catalog_check, commands[commands.index(["just", "generate"]) + 1 :])

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
