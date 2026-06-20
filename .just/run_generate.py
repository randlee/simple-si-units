#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


REQUIRED_MODULES = ("pandas", "numpy")


def missing_modules() -> list[str]:
    return [module for module in REQUIRED_MODULES if importlib.util.find_spec(module) is None]


def local_venv_python(repo_root: Path) -> Path | None:
    candidates = (
        repo_root / ".venv" / "bin" / "python",
        repo_root / ".venv" / "Scripts" / "python.exe",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    missing = missing_modules()
    if missing:
        venv_python = local_venv_python(repo_root)
        if venv_python is not None and Path(sys.executable) != venv_python:
            completed = subprocess.run([str(venv_python), __file__, *argv[1:]], cwd=repo_root)
            return completed.returncode
        print(
            "generate failed: missing Python modules required by code-generator: "
            + ", ".join(missing),
            file=sys.stderr,
        )
        return 2

    completed = subprocess.run(
        [sys.executable or "python3", str(repo_root / "code-generator/code_generator.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
        return completed.returncode

    formatted = subprocess.run(["cargo", "fmt", "--all"], cwd=repo_root)
    return formatted.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
