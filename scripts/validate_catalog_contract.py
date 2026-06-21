#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SAMPLE_CATALOG = ROOT / "catalog" / "examples" / "phase-a-sample-catalog.json"


class ValidationError(ValueError):
    pass


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def require_non_empty_string(value: Any, label: str) -> str:
    require(isinstance(value, str) and value.strip(), f"{label} must be a non-empty string")
    return value


def require_string_list(value: Any, label: str) -> list[str]:
    require(isinstance(value, list), f"{label} must be an array")
    rendered: list[str] = []
    for index, item in enumerate(value):
        rendered.append(require_non_empty_string(item, f"{label}[{index}]"))
    return rendered


def validate_conversion(conversion: Any, label: str) -> None:
    require(isinstance(conversion, dict), f"{label} must be an object")
    kind = require_non_empty_string(conversion.get("kind"), f"{label}.kind")
    require(kind in {"linear", "affine"}, f"{label}.kind must be `linear` or `affine`")
    require(isinstance(conversion.get("scale_to_base"), (int, float)), f"{label}.scale_to_base must be numeric")
    require("offset_to_base" in conversion, f"{label}.offset_to_base is required")
    offset = conversion.get("offset_to_base")
    if kind == "linear":
        require(offset is None, f"{label}.offset_to_base must be null for `linear` conversions")
    else:
        require(isinstance(offset, (int, float)), f"{label}.offset_to_base must be numeric for `affine` conversions")


def validate_unit(unit: Any, label: str) -> tuple[str, str]:
    require(isinstance(unit, dict), f"{label} must be an object")
    unit_code_id = require_non_empty_string(unit.get("unit_code_id"), f"{label}.unit_code_id")
    binary_unit_id = require_non_empty_string(unit.get("binary_unit_id"), f"{label}.binary_unit_id")
    require_non_empty_string(unit.get("unit_symbol"), f"{label}.unit_symbol")
    require_non_empty_string(unit.get("display_name"), f"{label}.display_name")
    reserved_word_alias = unit.get("reserved_word_alias")
    require(
        reserved_word_alias is None or (isinstance(reserved_word_alias, str) and reserved_word_alias.strip()),
        f"{label}.reserved_word_alias must be null or a non-empty string",
    )
    require_string_list(unit.get("aliases"), f"{label}.aliases")
    validate_conversion(unit.get("conversion"), f"{label}.conversion")
    return unit_code_id, binary_unit_id


def validate_dimension(dimension: Any, label: str) -> str:
    require(isinstance(dimension, dict), f"{label} must be an object")
    dimension_id = require_non_empty_string(dimension.get("dimension_id"), f"{label}.dimension_id")
    require_non_empty_string(dimension.get("public_type"), f"{label}.public_type")
    family = require_non_empty_string(dimension.get("family"), f"{label}.family")
    require(family in {"base", "geometry", "mechanical", "electromagnetic", "example"}, f"{label}.family is invalid")
    base_unit_code_id = require_non_empty_string(dimension.get("base_unit_code_id"), f"{label}.base_unit_code_id")

    json_forms = dimension.get("json_forms")
    require(isinstance(json_forms, dict), f"{label}.json_forms must be an object")
    require_string_list(json_forms.get("scalar_type_ids"), f"{label}.json_forms.scalar_type_ids")
    require_non_empty_string(
        json_forms.get("small_array_type_id_template"),
        f"{label}.json_forms.small_array_type_id_template",
    )
    require_non_empty_string(
        json_forms.get("buffer_type_id_template"),
        f"{label}.json_forms.buffer_type_id_template",
    )
    default_encoding = require_non_empty_string(json_forms.get("default_encoding"), f"{label}.json_forms.default_encoding")
    require(default_encoding in {"scalar", "array", "base64-le"}, f"{label}.json_forms.default_encoding is invalid")

    abi = dimension.get("abi")
    require(isinstance(abi, dict), f"{label}.abi must be an object")
    require_non_empty_string(abi.get("abi_name_stem"), f"{label}.abi.abi_name_stem")
    require_non_empty_string(abi.get("binary_schema_id"), f"{label}.abi.binary_schema_id")

    units = dimension.get("units")
    require(isinstance(units, list) and units, f"{label}.units must be a non-empty array")
    seen_unit_ids: set[str] = set()
    seen_binary_ids: set[str] = set()
    for index, unit in enumerate(units):
        unit_code_id, binary_unit_id = validate_unit(unit, f"{label}.units[{index}]")
        require(unit_code_id not in seen_unit_ids, f"{label} contains duplicate unit_code_id `{unit_code_id}`")
        require(binary_unit_id not in seen_binary_ids, f"{label} contains duplicate binary_unit_id `{binary_unit_id}`")
        seen_unit_ids.add(unit_code_id)
        seen_binary_ids.add(binary_unit_id)
    require(base_unit_code_id in seen_unit_ids, f"{label}.base_unit_code_id `{base_unit_code_id}` must exist in units[]")
    return dimension_id


def validate_catalog(payload: Any) -> None:
    require(isinstance(payload, dict), "catalog root must be an object")
    require_non_empty_string(payload.get("schema_version"), "schema_version")
    require_non_empty_string(payload.get("catalog_version"), "catalog_version")
    dimensions = payload.get("dimensions")
    require(isinstance(dimensions, list) and dimensions, "dimensions must be a non-empty array")

    seen_dimension_ids: set[str] = set()
    for index, dimension in enumerate(dimensions):
        dimension_id = validate_dimension(dimension, f"dimensions[{index}]")
        require(dimension_id not in seen_dimension_ids, f"duplicate dimension_id `{dimension_id}`")
        seen_dimension_ids.add(dimension_id)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate the units-x Phase A catalog contract.")
    parser.add_argument("catalog", nargs="?", default=SAMPLE_CATALOG.as_posix())
    args = parser.parse_args(argv[1:])

    path = Path(args.catalog)
    payload = read_json(path)
    validate_catalog(payload)
    print(f"catalog contract validation passed: {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
