#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERATED_PATHS = (
    "catalog/generated/units-catalog-summary.json",
    "catalog/generated/phase-b-conversion-coverage.json",
    "catalog/generated/phase-b-arithmetic-support.json",
    "crates/units-x/src/generated/catalog_metadata.rs",
    "crates/units-x/src/generated/conversion_metadata.rs",
    "crates/units-x/src/generated/ffi_contract_types.rs",
    "crates/units-x/src/generated/public_types.rs",
)


def main(argv: list[str]) -> int:
    generator_check = subprocess.run(
        [sys.executable or "python3", str(ROOT / "scripts" / "generate_catalog_artifacts.py"), "--mode", "check"],
        cwd=ROOT,
        check=False,
    )
    if generator_check.returncode != 0:
        return generator_check.returncode

    completed = subprocess.run(
        ["git", "status", "--porcelain=1", "--untracked-files=all", "--", *GENERATED_PATHS],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        return completed.returncode
    dirty_rows = [line for line in completed.stdout.splitlines() if line.strip()]
    if not dirty_rows:
        print("generated artifact cleanliness check passed")
        return 0
    for row in dirty_rows:
        print(row)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
