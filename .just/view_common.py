#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import shutil
from typing import Any


VIEW_ROOT = Path("artifacts/view")
FINDINGS_ROOT = Path("artifacts/findings")


def findings_dir(repo_root: Path, tool_name: str) -> Path:
    return repo_root / FINDINGS_ROOT / tool_name


def reset_findings_dir(repo_root: Path, tool_name: str) -> Path:
    target = findings_dir(repo_root, tool_name)
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)
    return target


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relative_artifact_path(repo_root: Path, path: Path) -> str:
    return path.relative_to(repo_root).as_posix()
