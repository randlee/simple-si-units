#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, contents: str) -> bool:
    if path.exists() and read_text(path) == contents:
        return False
    path.write_text(contents, encoding="utf-8", newline="\n")
    return True


def load_tool_versions() -> dict:
    return json.loads(read_text(ROOT / "tool-versions.json"))


def render_ci_workflow(tool_versions: dict) -> str:
    actions = tool_versions["github_actions"]
    pr_branches = ", ".join(f'"{branch}"' if "*" in branch or "/" in branch else branch for branch in actions["pull_request_branches"])
    push_branches = ", ".join(f'"{branch}"' if "*" in branch or "/" in branch else branch for branch in actions["push_branches"])
    runners = ", ".join(actions["runner_os"])
    return f"""name: CI

on:
  workflow_dispatch:
  pull_request:
    branches: [{pr_branches}]
  push:
    branches: [{push_branches}]

jobs:
  repo-ci:
    name: Repo CI (${{{{ matrix.os }}}})
    strategy:
      fail-fast: false
      matrix:
        os: [{runners}]
    runs-on: ${{{{ matrix.os }}}}
    env:
      PYTHONUTF8: "1"

    steps:
      - uses: actions/checkout@v5

      - name: Install Rust toolchain
        uses: dtolnay/rust-toolchain@{actions["rust_toolchain_action_ref"]}
        with:
          toolchain: "{actions["rust_toolchain"]}"
          components: clippy, rustfmt

      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: "{actions["python"]}"

      - name: Install .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: "{actions["dotnet_sdk"]}"

      - name: Install Python CI dependencies
        run: python -m pip install -r python/requirements-ci.txt

      - name: Install just
        run: cargo install just --locked --version {actions["just"]}

      - name: Install sc-lint
        run: cargo install sc-lint --locked --version {actions["sc_lint"]}

      - name: Install sc-lint-boundary
        run: cargo install sc-lint-boundary --locked --version {actions["sc_lint_boundary"]}

      - name: Run repo CI
        run: just ci
"""


def render_requirements(tool_versions: dict) -> str:
    return "\n".join(tool_versions["python_ci_requirements"]) + "\n"


def render_rust_toolchain(tool_versions: dict) -> str:
    rust = tool_versions["github_actions"]["rust_toolchain"]
    return f"""[toolchain]
channel = "{rust}"
components = ["clippy", "rustfmt"]
profile = "minimal"
"""


def render_global_json(tool_versions: dict) -> str:
    sdk = tool_versions["github_actions"]["dotnet_sdk"]
    payload = {
        "sdk": {
            "version": sdk,
            "rollForward": "disable",
        }
    }
    return json.dumps(payload, indent=2) + "\n"


def sync() -> list[str]:
    tool_versions = load_tool_versions()
    changed: list[str] = []
    outputs = {
        ROOT / ".github" / "workflows" / "ci.yml": render_ci_workflow(tool_versions),
        ROOT / "python" / "requirements-ci.txt": render_requirements(tool_versions),
        ROOT / "rust-toolchain.toml": render_rust_toolchain(tool_versions),
        ROOT / "global.json": render_global_json(tool_versions),
    }
    for path, contents in outputs.items():
        if write_text(path, contents):
            changed.append(path.relative_to(ROOT).as_posix())
    return changed


def check() -> list[str]:
    tool_versions = load_tool_versions()
    expected = {
        ".github/workflows/ci.yml": render_ci_workflow(tool_versions),
        "python/requirements-ci.txt": render_requirements(tool_versions),
        "rust-toolchain.toml": render_rust_toolchain(tool_versions),
        "global.json": render_global_json(tool_versions),
    }
    drifted: list[str] = []
    for relative, contents in expected.items():
        path = ROOT / relative
        if not path.exists() or read_text(path) != contents:
            drifted.append(relative)
    return drifted


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize repo toolchain/version pin files from tool-versions.json.")
    parser.add_argument("--check", action="store_true", help="Fail if generated files are out of sync.")
    args = parser.parse_args()

    if args.check:
        drifted = check()
        if drifted:
            print("tool version files are out of sync with tool-versions.json:")
            for path in drifted:
                print(f"  {path}")
            return 1
        print("tool version sync check passed")
        return 0

    changed = sync()
    if changed:
        print("synchronized tool version files from tool-versions.json:")
        for path in changed:
            print(f"  {path}")
    else:
        print("tool version files already synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
