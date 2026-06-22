#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from lint_common import discover_repo_root


VALID_SCOPES = ("all", "unit", "python", "dotnet", "integration", "rust", "help")
GENERATED_ARTIFACT_PATHS = (
    "catalog/generated/units-catalog-summary.json",
    "catalog/generated/phase-b-conversion-coverage.json",
    "crates/units-x/src/generated/catalog_metadata.rs",
    "crates/units-x/src/generated/conversion_metadata.rs",
    "crates/units-x/src/generated/ffi_contract_types.rs",
    "crates/units-x/src/generated/public_types.rs",
)


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


def generated_artifacts_are_dirty(repo_root: Path) -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain=1", "--untracked-files=all", "--", *GENERATED_ARTIFACT_PATHS],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        return True
    return bool(completed.stdout.strip())


def python_checks(repo_root: Path) -> list[list[str]]:
    python = sys.executable or "python3"
    return [
        [python, str(repo_root / ".just/run_pytests.py")],
        [python, str(repo_root / ".just/run_python_package_smoke.py")],
    ]


def reference_rust_test_commands(repo_root: Path) -> list[list[str]]:
    return [
        ["cargo", "test", "--manifest-path", str(repo_root / "reference" / "simple-si-units-core" / "Cargo.toml")],
        ["cargo", "test", "--manifest-path", str(repo_root / "reference" / "simple-si-units-macros" / "Cargo.toml")],
        ["cargo", "test", "--manifest-path", str(repo_root / "reference" / "simple-si-units" / "Cargo.toml"), "--all-features"],
    ]


def dotnet_test_projects(repo_root: Path) -> list[Path]:
    return sorted((repo_root / "dotnet").rglob("*Tests.csproj"))


def run_all(repo_root: Path) -> int:
    generated_were_dirty = generated_artifacts_are_dirty(repo_root)
    commands = [
        ["just", "clean"],
        [sys.executable or "python3", str(repo_root / ".just/check_version_sync.py")],
        [sys.executable or "python3", str(repo_root / "scripts/generate_catalog_artifacts.py"), "--mode", "check"],
        [sys.executable or "python3", str(repo_root / "scripts/sync_tool_versions.py"), "--check"],
        ["just", "generate"],
        [sys.executable or "python3", str(repo_root / ".just/run_lint.py"), "fast"],
        ["cargo", "test", "--workspace", "--all-features"],
    ]
    if generated_were_dirty:
        commands.insert(
            5,
            [sys.executable or "python3", str(repo_root / "scripts/generate_catalog_artifacts.py"), "--mode", "check"],
        )
    else:
        commands.insert(
            5,
            [sys.executable or "python3", str(repo_root / "scripts/check_generated_artifacts_clean.py")],
        )
    commands.extend(reference_rust_test_commands(repo_root))
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
    commands = [["cargo", "test", "--workspace", "--all-features"]]
    commands.extend(reference_rust_test_commands(repo_root))
    for command in commands:
        code = run_command(command, repo_root)
        if code != 0:
            return code
    return 0


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
