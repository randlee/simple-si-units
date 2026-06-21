#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SAMPLE_CATALOG = ROOT / "catalog" / "examples" / "phase-a-sample-catalog.json"
CATALOG_SCHEMA = ROOT / "catalog" / "schema" / "units-catalog.schema.json"


class ValidationError(ValueError):
    pass


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def require_non_blank_string(value: Any, label: str) -> None:
    require(isinstance(value, str) and value.strip(), f"{label} must be a non-blank string")


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
    require_non_blank_string(dimension["dimension_id"], f"{label}.dimension_id")
    require_non_blank_string(dimension["public_type"], f"{label}.public_type")
    require_non_blank_string(dimension["base_unit_code_id"], f"{label}.base_unit_code_id")
    dimension_id = str(dimension["dimension_id"])
    base_unit_code_id = str(dimension["base_unit_code_id"])
    json_forms = dimension["json_forms"]
    require_non_blank_string(json_forms["small_array_type_id_template"], f"{label}.json_forms.small_array_type_id_template")
    require_non_blank_string(json_forms["buffer_type_id_template"], f"{label}.json_forms.buffer_type_id_template")
    require_non_blank_string(json_forms["default_encoding"], f"{label}.json_forms.default_encoding")
    for index, scalar_type_id in enumerate(json_forms["scalar_type_ids"]):
        require_non_blank_string(scalar_type_id, f"{label}.json_forms.scalar_type_ids[{index}]")

    abi = dimension["abi"]
    require_non_blank_string(abi["abi_name_stem"], f"{label}.abi.abi_name_stem")
    require_non_blank_string(abi["binary_schema_id"], f"{label}.abi.binary_schema_id")

    units = dimension["units"]
    seen_unit_ids: set[str] = set()
    seen_binary_ids: set[str] = set()
    for index, unit in enumerate(units):
        require_non_blank_string(unit["unit_code_id"], f"{label}.units[{index}].unit_code_id")
        require_non_blank_string(unit["unit_symbol"], f"{label}.units[{index}].unit_symbol")
        require_non_blank_string(unit["display_name"], f"{label}.units[{index}].display_name")
        reserved_word_alias = unit["reserved_word_alias"]
        require(
            reserved_word_alias is None
            or (isinstance(reserved_word_alias, str) and reserved_word_alias.strip()),
            f"{label}.units[{index}].reserved_word_alias must be null or a non-blank string",
        )
        for alias_index, alias in enumerate(unit["aliases"]):
            require_non_blank_string(alias, f"{label}.units[{index}].aliases[{alias_index}]")
        unit_code_id = str(unit["unit_code_id"])
        binary_unit_id = str(unit["binary_unit_id"])
        require(unit_code_id not in seen_unit_ids, f"{label} contains duplicate unit_code_id `{unit_code_id}`")
        require(binary_unit_id not in seen_binary_ids, f"{label} contains duplicate binary_unit_id `{binary_unit_id}`")
        seen_unit_ids.add(unit_code_id)
        seen_binary_ids.add(binary_unit_id)
    require(base_unit_code_id in seen_unit_ids, f"{label}.base_unit_code_id `{base_unit_code_id}` must exist in units[]")
    return dimension_id


def validate_catalog(payload: Any) -> None:
    validate_schema(payload)
    require_non_blank_string(payload["schema_version"], "schema_version")
    require_non_blank_string(payload["catalog_version"], "catalog_version")
    dimensions = payload["dimensions"]

    seen_dimension_ids: set[str] = set()
    for index, dimension in enumerate(dimensions):
        dimension_id = validate_dimension_invariants(dimension, f"dimensions[{index}]")
        require(dimension_id not in seen_dimension_ids, f"duplicate dimension_id `{dimension_id}`")
        seen_dimension_ids.add(dimension_id)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate the units-x Phase A catalog contract.")
    parser.add_argument("catalog", nargs="?", default=SAMPLE_CATALOG.as_posix())
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
