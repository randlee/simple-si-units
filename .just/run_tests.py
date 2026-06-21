#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from lint_common import discover_repo_root


VALID_SCOPES = ("all", "unit", "python", "dotnet", "integration", "rust", "help")


def print_help() -> None:
    print("Test scopes:")
    print("  just test           Run the full repo test pass.")
    print("  just test all       Alias for the full repo test pass.")
    print("  just test unit      Run Rust unit tests.")
    print("  just test python    Run Python helper-script tests and native wheel smoke.")
    print("  just test dotnet    Run .NET tests when configured.")
    print("  just test integration  Run integration-style tests.")
    print("  just test rust      Run all Rust workspace tests.")


def run_command(command: list[str], repo_root: Path) -> int:
    completed = subprocess.run(command, cwd=repo_root)
    return completed.returncode


def python_checks(repo_root: Path) -> list[list[str]]:
    python = sys.executable or "python3"
    return [
        [python, str(repo_root / ".just/run_pytests.py")],
        [python, str(repo_root / ".just/run_python_package_smoke.py")],
    ]


def dotnet_test_projects(repo_root: Path) -> list[Path]:
    return sorted((repo_root / "dotnet").rglob("*Tests.csproj"))


def run_all(repo_root: Path) -> int:
    commands = [
        ["just", "clean"],
        [sys.executable or "python3", str(repo_root / ".just/check_version_sync.py")],
        ["just", "generate"],
        [sys.executable or "python3", str(repo_root / ".just/run_lint.py"), "fast"],
        ["cargo", "test", "--workspace", "--all-features"],
    ]
    commands.extend(python_checks(repo_root))
    for command in commands:
        code = run_command(command, repo_root)
        if code != 0:
            return code
    return run_dotnet(repo_root)


def run_unit(repo_root: Path) -> int:
    return run_command(["cargo", "test", "--workspace", "--all-features", "--lib"], repo_root)


def run_python(repo_root: Path) -> int:
    for command in python_checks(repo_root):
        code = run_command(command, repo_root)
        if code != 0:
            return code
    return 0


def run_dotnet(repo_root: Path) -> int:
    projects = dotnet_test_projects(repo_root)
    if not projects:
        project = repo_root / "dotnet" / "src" / "UnitsX" / "UnitsX.csproj"
        if not project.exists():
            print("dotnet tests skipped: no .NET project files under dotnet/")
            return 0
        return run_command(["dotnet", "build", str(project), "--nologo"], repo_root)
    return run_command(["dotnet", "test", "dotnet"], repo_root)


def run_integration(repo_root: Path) -> int:
    return run_command(["cargo", "test", "--workspace", "--all-features", "--tests"], repo_root)


def run_rust(repo_root: Path) -> int:
    return run_command(["cargo", "test", "--workspace", "--all-features"], repo_root)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run repo test scopes.")
    parser.add_argument("scope", nargs="?", default="all")
    parser.add_argument("--root", help="Repo root to inspect.")
    args = parser.parse_args(argv[1:])

    if args.scope == "help":
        print_help()
        return 0

    if args.scope not in VALID_SCOPES:
        valid = ", ".join(VALID_SCOPES)
        print(f"unknown test scope: {args.scope}; expected one of: {valid}", file=sys.stderr)
        return 2

    repo_root = discover_repo_root(args.root)
    if args.scope == "all":
        return run_all(repo_root)
    if args.scope == "unit":
        return run_unit(repo_root)
    if args.scope == "python":
        return run_python(repo_root)
    if args.scope == "dotnet":
        return run_dotnet(repo_root)
    if args.scope == "integration":
        return run_integration(repo_root)
    return run_rust(repo_root)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
