#!/usr/bin/env python3
from __future__ import annotations

from contextlib import contextmanager
import shutil
import tempfile
import tomllib
from pathlib import Path


def load_root_manifest(repo_root: Path) -> dict:
    return tomllib.loads((repo_root / "Cargo.toml").read_text(encoding="utf-8"))


def shipped_workspace_toml(repo_root: Path) -> str:
    manifest = load_root_manifest(repo_root)
    package = manifest["workspace"]["package"]
    lines = [
        "[workspace]",
        'members = ["crates/units-x", "crates/units-x-python"]',
        'resolver = "2"',
        "",
        "[workspace.package]",
        f'version = "{package["version"]}"',
        f'edition = "{package["edition"]}"',
        f'license = "{package["license"]}"',
        f'repository = "{package["repository"]}"',
        f'homepage = "{package["homepage"]}"',
        f'rust-version = "{package["rust-version"]}"',
    ]
    authors = package.get("authors", [])
    if authors:
        quoted = ", ".join(f'"{author}"' for author in authors)
        lines.append(f"authors = [{quoted}]")
    return "\n".join(lines) + "\n"


def prepare_boundary_scope(repo_root: Path, scope_root: Path) -> None:
    crate_dst = scope_root / "crates" / "units-x"
    crate_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(repo_root / "crates" / "units-x", crate_dst, dirs_exist_ok=True)
    shutil.copytree(
        repo_root / "crates" / "units-x-python",
        scope_root / "crates" / "units-x-python",
        dirs_exist_ok=True,
    )

    boundaries_root = scope_root / "boundaries"
    boundary_dst = boundaries_root / "units-x"
    boundaries_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(repo_root / "boundaries" / "units-x", boundary_dst, dirs_exist_ok=True)
    shutil.copytree(
        repo_root / "boundaries" / "units-x-python",
        boundaries_root / "units-x-python",
        dirs_exist_ok=True,
    )
    shutil.copy2(repo_root / "boundaries" / "planning.toml", boundaries_root / "planning.toml")

    (scope_root / "Cargo.toml").write_text(
        shipped_workspace_toml(repo_root),
        encoding="utf-8",
        newline="\n",
    )


@contextmanager
def shipped_scope_workspace(repo_root: Path):
    with tempfile.TemporaryDirectory(prefix="units-x-shipped-scope-") as tmpdir:
        scope_root = Path(tmpdir)
        prepare_boundary_scope(repo_root, scope_root)
        yield scope_root
