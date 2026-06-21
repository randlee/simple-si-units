#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys

from lint_common import discover_repo_root
from scope_workspace import shipped_scope_workspace


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run shipped-scope Rust lint commands.")
    parser.add_argument("tool", choices=("check", "clippy"))
    parser.add_argument("--root", help="Repo root to inspect.")
    args = parser.parse_args(argv[1:])

    repo_root = discover_repo_root(args.root)
    with shipped_scope_workspace(repo_root) as scope_root:
        command = ["sc-lint", "--root", str(scope_root), args.tool, "native"]
        completed = subprocess.run(command, cwd=repo_root)
        return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
