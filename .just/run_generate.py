#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    synchronized = subprocess.run(
        [sys.executable or "python3", str(repo_root / "scripts" / "sync_version_files.py")],
        cwd=repo_root,
    )
    if synchronized.returncode != 0:
        return synchronized.returncode

    completed = subprocess.run(
        [sys.executable or "python3", str(repo_root / "scripts" / "validate_catalog_contract.py")],
        cwd=repo_root,
    )
    if completed.returncode != 0:
        return completed.returncode

    formatted = subprocess.run(["cargo", "fmt", "--all"], cwd=repo_root)
    return formatted.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
