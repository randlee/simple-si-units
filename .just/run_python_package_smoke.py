#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from lint_common import discover_repo_root


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> int:
    return subprocess.run(command, cwd=cwd, env=env).returncode


def build_and_import(repo_root: Path) -> int:
    python = sys.executable or "python3"
    python_root = repo_root / "python"
    dist_dir = python_root / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    for wheel in dist_dir.glob("units_x-*.whl"):
        wheel.unlink()

    build = [
        python,
        "-m",
        "build",
        "--wheel",
        "--outdir",
        str(dist_dir),
        str(python_root),
    ]
    if run(build, cwd=repo_root) != 0:
        return 1

    wheels = sorted(dist_dir.glob("units_x-*.whl"))
    if not wheels:
        print("maturin build did not produce a units_x wheel", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="units-x-python-smoke-") as tmpdir:
        site_dir = Path(tmpdir) / "site"
        site_dir.mkdir(parents=True, exist_ok=True)
        install = [
            python,
            "-m",
            "pip",
            "install",
            "--force-reinstall",
            "--no-deps",
            "--target",
            str(site_dir),
            str(wheels[-1]),
        ]
        if run(install, cwd=repo_root) != 0:
            return 1

        env = dict(os.environ)
        env["PYTHONPATH"] = str(site_dir)
        smoke = [
            python,
            "-c",
            (
                "import units_x; "
                "import units_x._native as native; "
                "assert native.version() == units_x.__version__; "
                "assert native.__version__ == units_x.__version__"
            ),
        ]
        return run(smoke, cwd=Path(tmpdir), env=env)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build and import the units-x Python native package.")
    parser.add_argument("--root", help="Repo root to inspect.")
    args = parser.parse_args(argv[1:])
    repo_root = discover_repo_root(args.root)
    return build_and_import(repo_root)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
