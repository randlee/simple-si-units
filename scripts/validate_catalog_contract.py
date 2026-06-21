#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
PRODUCTION_CATALOG = ROOT / "catalog" / "units-catalog.json"
SAMPLE_CATALOG = ROOT / "catalog" / "examples" / "phase-a-sample-catalog.json"
CATALOG_SCHEMA = ROOT / "catalog" / "schema" / "units-catalog.schema.json"


class ValidationError(ValueError):
    pass


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_schema(payload: Any) -> None:
    schema = read_json(CATALOG_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise ValidationError(f"schema validation failed at {location}: {first.message}")


def validate_dimension_invariants(dimension: Any, label: str) -> str:
    require(isinstance(dimension, dict), f"{label} must be an object")
    dimension_id = str(dimension["dimension_id"])
    base_unit_code_id = str(dimension["base_unit_code_id"])
    units = dimension["units"]
    seen_unit_ids: set[str] = set()
    seen_binary_ids: set[str] = set()
    for index, unit in enumerate(units):
        unit_code_id = str(unit["unit_code_id"])
        binary_unit_id = str(unit["binary_unit_id"])
        expected_binary_id = f"{dimension_id}.{unit_code_id}"
        require(unit_code_id not in seen_unit_ids, f"{label} contains duplicate unit_code_id `{unit_code_id}`")
        require(binary_unit_id not in seen_binary_ids, f"{label} contains duplicate binary_unit_id `{binary_unit_id}`")
        require(
            binary_unit_id == expected_binary_id,
            f"{label}.units[{index}].binary_unit_id `{binary_unit_id}` must match `{expected_binary_id}`",
        )
        seen_unit_ids.add(unit_code_id)
        seen_binary_ids.add(binary_unit_id)
    require(base_unit_code_id in seen_unit_ids, f"{label}.base_unit_code_id `{base_unit_code_id}` must exist in units[]")
    return dimension_id


def validate_catalog(payload: Any) -> None:
    validate_schema(payload)
    dimensions = payload["dimensions"]

    seen_dimension_ids: set[str] = set()
    for index, dimension in enumerate(dimensions):
        dimension_id = validate_dimension_invariants(dimension, f"dimensions[{index}]")
        require(dimension_id not in seen_dimension_ids, f"duplicate dimension_id `{dimension_id}`")
        seen_dimension_ids.add(dimension_id)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate the units-x Phase A catalog contract.")
    parser.add_argument("catalog", nargs="?", default=PRODUCTION_CATALOG.as_posix())
    args = parser.parse_args(argv[1:])

    path = Path(args.catalog)
    payload = read_json(path)
    validate_catalog(payload)
    try:
        rendered = path.relative_to(ROOT).as_posix()
    except ValueError:
        rendered = path.as_posix()
    print(f"catalog contract validation passed: {rendered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
