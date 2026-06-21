#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERATED_PATHS = (
    "catalog/generated/units-catalog-summary.json",
    "crates/units-x/src/generated/catalog_metadata.rs",
)


def main(argv: list[str]) -> int:
    completed = subprocess.run(
        ["git", "diff", "--exit-code", "HEAD", "--", *GENERATED_PATHS],
        cwd=ROOT,
        check=False,
    )
    if completed.returncode == 0:
        print("generated artifact cleanliness check passed")
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
