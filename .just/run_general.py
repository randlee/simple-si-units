#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from lint_common import discover_repo_root
from print_help import render_topic_help


VALID_ACTIONS = ("generate", "build", "clean", "version", "ci")
VALID_MODES = ("run", "help")


def run_command(command: list[str], repo_root: Path) -> int:
    completed = subprocess.run(command, cwd=repo_root)
    return completed.returncode


def print_action_help(action: str) -> int:
    text = render_topic_help(action)
    if text.startswith("unknown help topic:"):
        print(text, end="", file=sys.stderr)
        return 2
    print(text, end="")
    return 0


def run_action(action: str, repo_root: Path) -> int:
    python = sys.executable or "python3"
    actions: dict[str, list[list[str]]] = {
        "generate": [[python, str(repo_root / ".just/run_generate.py")]],
        "build": [
            [python, str(repo_root / ".just/run_generate.py")],
            [python, str(repo_root / ".just/run_lint.py"), "fast"],
            ["cargo", "build", "--workspace", "--all-features"],
        ],
        "clean": [["cargo", "clean"]],
        "version": [[python, str(repo_root / ".just/check_version_sync.py")]],
        "ci": [[python, str(repo_root / ".just/run_tests.py"), "all"]],
    }
    for command in actions[action]:
        code = run_command(command, repo_root)
        if code != 0:
            return code
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run repo general recipes.")
    parser.add_argument("action")
    parser.add_argument("mode", nargs="?", default="run")
    parser.add_argument("--root", help="Repo root to inspect.")
    args = parser.parse_args(argv[1:])

    if args.action not in VALID_ACTIONS:
        valid = ", ".join(VALID_ACTIONS)
        print(f"unknown action: {args.action}; expected one of: {valid}", file=sys.stderr)
        return 2

    if args.mode not in VALID_MODES:
        valid = ", ".join(VALID_MODES)
        print(f"unknown mode: {args.mode}; expected one of: {valid}", file=sys.stderr)
        return 2

    if args.mode == "help":
        return print_action_help(args.action)

    repo_root = discover_repo_root(args.root)
    return run_action(args.action, repo_root)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
