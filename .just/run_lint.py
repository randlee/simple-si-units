#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import argparse
import subprocess
import sys
import time

from lint_common import discover_repo_root
from lint_common import format_duration
from lint_common import make_log_path
from lint_common import relative_log_path
from lint_common import write_log


TASK_PROFILES = {
    "fast": ("fmt", "version", "check", "identity-literals"),
    "full": ("fmt", "version", "check", "identity-literals", "clippy", "pytests"),
    "fmt": ("fmt",),
    "version": ("version",),
    "check": ("check",),
    "clippy": ("clippy",),
    "sc-boundary": ("sc-boundary",),
    "identity-literals": ("identity-literals",),
    "pytests": ("pytests",),
}


def print_help() -> None:
    print("Lint targets:")
    print("  just lint             Run the default full lint profile.")
    print("  just lint fast        Run the fast lint subset.")
    print("  just lint full        Run the stronger local lint profile.")
    print("  just lint fmt         Run only the format check.")
    print("  just lint version     Run only the version synchronization check.")
    print("  just lint check       Run only `sc-lint check native`.")
    print("  just lint clippy      Run only `sc-lint clippy native`.")
    print("  just lint sc-boundary Run the boundary analyzer wrapper.")
    print("  just lint identity-literals  Run the canonical literal lint.")
    print("  just lint pytests     Run the Python helper-script unit tests.")


@dataclass(frozen=True)
class LintTask:
    name: str
    command: list[str]


def python_executable() -> str:
    return sys.executable or ("python" if sys.platform == "win32" else "python3")


def build_tasks(repo_root: Path) -> dict[str, LintTask]:
    py = python_executable()
    return {
        "fmt": LintTask("fmt", ["just", "_fmt-check"]),
        "version": LintTask("version", [py, str(repo_root / ".just/check_version_sync.py")]),
        "check": LintTask("check", ["sc-lint", "--root", str(repo_root), "check", "native"]),
        "clippy": LintTask("clippy", ["sc-lint", "--root", str(repo_root), "clippy", "native"]),
        "sc-boundary": LintTask("sc-boundary", [py, str(repo_root / ".just/lint_sc_boundary.py")]),
        "identity-literals": LintTask(
            "identity-literals",
            [py, str(repo_root / ".just/lint_identity_literals.py")],
        ),
        "pytests": LintTask("pytests", [py, str(repo_root / ".just/run_pytests.py")]),
    }


def resolve_task_names(target: str) -> tuple[str, ...]:
    try:
        return TASK_PROFILES[target]
    except KeyError as exc:
        valid = ", ".join(sorted(TASK_PROFILES))
        raise ValueError(f"unknown lint target: {target}; expected one of: {valid}") from exc


def build_transcript(task: LintTask, repo_root: Path, completed: subprocess.CompletedProcess[str], duration_seconds: float) -> list[str]:
    return [
        f"lint: {task.name}",
        f"repo_root: {repo_root}",
        f"recorded_at_utc: {datetime.now(timezone.utc).isoformat()}",
        f"duration: {format_duration(duration_seconds)}",
        f"command: {' '.join(task.command)}",
        f"exit_code: {completed.returncode}",
        "",
        "stdout:",
        completed.stdout.rstrip(),
        "",
        "stderr:",
        completed.stderr.rstrip(),
    ]


def run_task(task: LintTask, repo_root: Path) -> int:
    started_at = datetime.now(timezone.utc)
    start_time = time.perf_counter()
    completed = subprocess.run(
        task.command,
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    duration_seconds = time.perf_counter() - start_time
    log_path = make_log_path(repo_root, task.name, started_at)
    write_log(log_path, build_transcript(task, repo_root, completed, duration_seconds))

    if completed.returncode == 0:
        print(f"{task.name} passed [{format_duration(duration_seconds)}]")
        return 0

    print(f"{task.name} failed [{format_duration(duration_seconds)}]")
    for stream in (completed.stdout, completed.stderr):
        for line in stream.splitlines():
            stripped = line.strip()
            if stripped:
                print(f"  {stripped}")
                break
        else:
            continue
        break
    print(f"  full log: {relative_log_path(repo_root, log_path)}")
    return completed.returncode


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run repo lint targets.")
    parser.add_argument("target", nargs="?", default="full")
    parser.add_argument("--root", help="Repo root to inspect.")
    args = parser.parse_args(argv[1:])
    repo_root = discover_repo_root(args.root)
    if args.target == "help":
        print_help()
        return 0
    try:
        task_names = resolve_task_names(args.target)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    tasks = build_tasks(repo_root)
    failures = 0
    for task_name in task_names:
        failures += 1 if run_task(tasks[task_name], repo_root) != 0 else 0

    if failures:
        print(f"lint failed: {failures} check(s) failed")
        return 1

    print(f"lint passed: {len(task_names)} check(s) succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
