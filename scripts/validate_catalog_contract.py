#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from json import JSONDecodeError
from pathlib import Path
import sys
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
PRODUCTION_CATALOG = ROOT / "catalog" / "units-catalog.json"
SAMPLE_CATALOG = ROOT / "catalog" / "examples" / "phase-a-sample-catalog.json"
CATALOG_SCHEMA = ROOT / "catalog" / "schema" / "units-catalog.schema.json"
RUST_KEYWORDS = {
    "Self",
    "abstract",
    "as",
    "async",
    "await",
    "become",
    "box",
    "break",
    "const",
    "continue",
    "crate",
    "do",
    "dyn",
    "else",
    "enum",
    "extern",
    "false",
    "final",
    "fn",
    "for",
    "if",
    "impl",
    "in",
    "let",
    "loop",
    "macro",
    "match",
    "mod",
    "move",
    "mut",
    "override",
    "priv",
    "pub",
    "ref",
    "return",
    "self",
    "static",
    "struct",
    "super",
    "trait",
    "true",
    "try",
    "type",
    "typeof",
    "unsafe",
    "unsized",
    "use",
    "virtual",
    "where",
    "while",
    "yield",
}


class ValidationError(ValueError):
    def __init__(self, code: str, message: str, location: str = "<root>") -> None:
        super().__init__(message)
        self.code = code
        self.location = location

    def to_envelope(self) -> dict[str, str]:
        return {
            "code": self.code,
            "location": self.location,
            "message": str(self),
        }


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str, location: str = "<root>") -> None:
    if not condition:
        raise ValidationError("catalog_invariant_failed", message, location)


def is_valid_rust_identifier(value: str) -> bool:
    if not value:
        return False
    if value in RUST_KEYWORDS:
        return False
    if value[0].isdigit():
        return False
    return all(char.isascii() and (char.isalnum() or char == "_") for char in value)


def validate_schema(payload: Any) -> None:
    schema = read_json(CATALOG_SCHEMA)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise ValidationError("schema_validation_failed", first.message, location)


def validate_dimension_invariants(dimension: Any, label: str) -> tuple[str, str, list[tuple[str, str]]]:
    require(isinstance(dimension, dict), f"{label} must be an object")
    dimension_id = str(dimension["dimension_id"])
    canonical_dimension_id = str(dimension["canonical_dimension_id"])
    base_unit_code_id = str(dimension["base_unit_code_id"])
    units = dimension["units"]
    seen_unit_ids: set[str] = set()
    seen_binary_ids: set[str] = set()
    seen_marker_names: set[str] = set()
    marker_names: list[tuple[str, str]] = []
    for index, unit in enumerate(units):
        unit_code_id = str(unit["unit_code_id"])
        binary_unit_id = str(unit["binary_unit_id"])
        marker_name = str(unit["reserved_word_alias"] or unit_code_id)
        expected_binary_id = f"{dimension_id}.{unit_code_id}"
        require(
            unit_code_id not in seen_unit_ids,
            f"{label} contains duplicate unit_code_id `{unit_code_id}`",
            f"{label}.units[{index}].unit_code_id",
        )
        require(
            binary_unit_id not in seen_binary_ids,
            f"{label} contains duplicate binary_unit_id `{binary_unit_id}`",
            f"{label}.units[{index}].binary_unit_id",
        )
        require(
            binary_unit_id == expected_binary_id,
            f"{label}.units[{index}].binary_unit_id `{binary_unit_id}` must match `{expected_binary_id}`",
            f"{label}.units[{index}].binary_unit_id",
        )
        require(
            is_valid_rust_identifier(marker_name),
            f"{label}.units[{index}] resolves to invalid Rust marker `{marker_name}`; use reserved_word_alias when needed",
            f"{label}.units[{index}]",
        )
        require(
            marker_name not in seen_marker_names,
            f"{label} contains duplicate generated Rust marker `{marker_name}`",
            f"{label}.units[{index}]",
        )
        seen_unit_ids.add(unit_code_id)
        seen_binary_ids.add(binary_unit_id)
        seen_marker_names.add(marker_name)
        marker_names.append((marker_name, f"{label}.units[{index}]"))
    require(
        base_unit_code_id in seen_unit_ids,
        f"{label}.base_unit_code_id `{base_unit_code_id}` must exist in units[]",
        f"{label}.base_unit_code_id",
    )
    return dimension_id, canonical_dimension_id, marker_names


def validate_conversion_policies(payload: Any, dimensions: list[Any]) -> None:
    policies = payload["conversion_policies"]
    policy_rows = policies["policies"]
    seen_policy_ids: set[str] = set()
    for index, row in enumerate(policy_rows):
        policy_id = str(row["policy_id"])
        require(
            policy_id not in seen_policy_ids,
            f"conversion_policies.policies[{index}].policy_id `{policy_id}` is duplicated",
            f"conversion_policies.policies[{index}].policy_id",
        )
        seen_policy_ids.add(policy_id)
        guard = row["infallibility_guard"]
        fallback = row["fallback_policy_id"]
        if guard is None:
            require(
                fallback is None,
                f"conversion_policies.policies[{index}] cannot declare fallback_policy_id without infallibility_guard",
                f"conversion_policies.policies[{index}].fallback_policy_id",
            )
        else:
            require(
                fallback is not None,
                f"conversion_policies.policies[{index}] with infallibility_guard must declare fallback_policy_id",
                f"conversion_policies.policies[{index}].fallback_policy_id",
            )
    for index, row in enumerate(policy_rows):
        fallback = row["fallback_policy_id"]
        if fallback is not None:
            require(
                fallback in seen_policy_ids,
                f"conversion_policies.policies[{index}].fallback_policy_id `{fallback}` must reference an existing policy",
                f"conversion_policies.policies[{index}].fallback_policy_id",
            )

    observed_storages = {
        type_id.rsplit("_", maxsplit=1)[1]
        for dimension in dimensions
        for type_id in dimension["json_forms"]["scalar"]["type_ids"]
    }
    required_pairs = {
        (source_storage, target_storage)
        for source_storage in observed_storages
        for target_storage in observed_storages
    }

    same_public_type = policies["same_public_type"]
    require(
        same_public_type["identity_policy_id"] in seen_policy_ids,
        "conversion_policies.same_public_type.identity_policy_id must reference an existing policy",
        "conversion_policies.same_public_type.identity_policy_id",
    )

    for section_name in ("same_public_type", "same_canonical_dimension", "reciprocal_bridge"):
        section = policies[section_name]
        seen_pairs: set[tuple[str, str]] = set()
        for index, row in enumerate(section["storage_pair_policies"]):
            pair = (str(row["source_storage"]), str(row["target_storage"]))
            require(
                row["policy_id"] in seen_policy_ids,
                f"conversion_policies.{section_name}.storage_pair_policies[{index}].policy_id `{row['policy_id']}` must reference an existing policy",
                f"conversion_policies.{section_name}.storage_pair_policies[{index}].policy_id",
            )
            require(
                pair not in seen_pairs,
                f"conversion_policies.{section_name} duplicates storage pair `{pair[0]}->{pair[1]}`",
                f"conversion_policies.{section_name}.storage_pair_policies[{index}]",
            )
            seen_pairs.add(pair)
        missing_pairs = sorted(required_pairs - seen_pairs)
        require(
            not missing_pairs,
            f"conversion_policies.{section_name} must define every observed storage pair; missing {missing_pairs}",
            f"conversion_policies.{section_name}.storage_pair_policies",
        )


def validate_catalog(payload: Any) -> None:
    validate_schema(payload)
    dimensions = payload["dimensions"]
    bridges = payload["bridges"]
    validate_conversion_policies(payload, dimensions)

    seen_dimension_ids: set[str] = set()
    canonical_dimension_ids: list[tuple[str, str]] = []
    seen_marker_names: set[str] = set()
    seen_public_types: set[str] = set()
    for index, dimension in enumerate(dimensions):
        dimension_id, canonical_dimension_id, marker_names = validate_dimension_invariants(dimension, f"dimensions[{index}]")
        public_type = str(dimension["public_type"])
        require(dimension_id not in seen_dimension_ids, f"duplicate dimension_id `{dimension_id}`", f"dimensions[{index}].dimension_id")
        require(
            public_type not in seen_public_types,
            f"duplicate public_type `{public_type}`",
            f"dimensions[{index}].public_type",
        )
        seen_dimension_ids.add(dimension_id)
        seen_public_types.add(public_type)
        canonical_dimension_ids.append((canonical_dimension_id, f"dimensions[{index}].canonical_dimension_id"))
        for marker_name, location in marker_names:
            require(
                marker_name not in seen_marker_names,
                f"duplicate generated Rust marker `{marker_name}` across catalog dimensions",
                location,
            )
            seen_marker_names.add(marker_name)

    for canonical_dimension_id, location in canonical_dimension_ids:
        require(
            canonical_dimension_id in seen_dimension_ids,
            f"{location} `{canonical_dimension_id}` must match an existing dimension_id",
            location,
        )

    seen_bridges: set[tuple[str, str, str]] = set()
    for index, bridge in enumerate(bridges):
        kind = str(bridge["kind"])
        left_public_type = str(bridge["left_public_type"])
        right_public_type = str(bridge["right_public_type"])
        require(
            left_public_type in seen_public_types,
            f"bridges[{index}].left_public_type `{left_public_type}` must reference an existing public_type",
            f"bridges[{index}].left_public_type",
        )
        require(
            right_public_type in seen_public_types,
            f"bridges[{index}].right_public_type `{right_public_type}` must reference an existing public_type",
            f"bridges[{index}].right_public_type",
        )
        require(
            left_public_type != right_public_type,
            f"bridges[{index}] must connect two distinct public types",
            f"bridges[{index}]",
        )
        bridge_key = (kind, *sorted((left_public_type, right_public_type)))
        require(
            bridge_key not in seen_bridges,
            f"duplicate bridge `{kind}` between `{left_public_type}` and `{right_public_type}`",
            f"bridges[{index}]",
        )
        seen_bridges.add(bridge_key)

    distance = next((dimension for dimension in dimensions if dimension["dimension_id"] == "distance"), None)
    require(distance is not None, "catalog must include the bootstrap `distance` dimension", "dimensions")
    require(
        any(unit["unit_code_id"] == "mm" for unit in distance["units"]),
        "distance dimension must include bootstrap unit_code_id `mm`",
        "dimensions.distance.units",
    )
    require(
        any(type_id.endswith("_i32") for type_id in distance["json_forms"]["scalar"]["type_ids"]),
        "distance dimension must include an `_i32` scalar type id for the Phase A FFI bootstrap exemplar",
        "dimensions.distance.json_forms.scalar.type_ids",
    )
    require(
        any(
            bridge["kind"] == "reciprocal"
            and {bridge["left_public_type"], bridge["right_public_type"]} == {"Distance", "Diopter"}
            for bridge in bridges
        ),
        "catalog must include the reciprocal bridge between Distance and Diopter",
        "bridges",
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate the units-x Phase A catalog contract.")
    parser.add_argument("catalog", nargs="?", default=PRODUCTION_CATALOG.as_posix())
    args = parser.parse_args(argv[1:])

    path = Path(args.catalog)
    try:
        payload = read_json(path)
        validate_catalog(payload)
    except ValidationError as error:
        print(json.dumps(error.to_envelope(), sort_keys=True), file=sys.stderr)
        return 1
    except FileNotFoundError as error:
        envelope = ValidationError("catalog_read_failed", str(error), path.as_posix()).to_envelope()
        print(json.dumps(envelope, sort_keys=True), file=sys.stderr)
        return 1
    except JSONDecodeError as error:
        envelope = ValidationError("catalog_json_decode_failed", error.msg, path.as_posix()).to_envelope()
        print(json.dumps(envelope, sort_keys=True), file=sys.stderr)
        return 1
    try:
        rendered = path.relative_to(ROOT).as_posix()
    except ValueError:
        rendered = path.as_posix()
    print(f"catalog contract validation passed: {rendered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
