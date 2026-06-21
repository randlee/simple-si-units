# Master Catalog Contract

## Purpose

This document defines the `units-x` master catalog contract that later
generation work will consume.

It is the prose companion to
[../../catalog/schema/units-catalog.schema.json](../../catalog/schema/units-catalog.schema.json)
and the sample data in
[../../catalog/examples/phase-a-sample-catalog.json](../../catalog/examples/phase-a-sample-catalog.json).

## Scope References

- REQ-UX-006
- REQ-UX-009
- REQ-UX-010
- REQ-UX-017
- REQ-UX-018
- REQ-UX-029
- REQ-UX-032
- REQ-UX-034
- REQ-UX-035
- REQ-UX-040
- NFR-UX-008
- NFR-UX-013
- ADR-UX-003
- ADR-UX-010
- ADR-UX-012
- ADR-UX-015
- ADR-UX-017

## Catalog Shape

The catalog root contains:

- `schema_version`
- `catalog_version`
- `dimensions`

Each `dimensions[]` entry owns:

- `dimension_id`
- `family`
- `public_type`
- `base_unit_code_id`
- `json_forms`
- `abi`
- `units`

Each `units[]` entry owns:

- `unit_code_id`
- `unit_symbol`
- `display_name`
- `binary_unit_id`
- `reserved_word_alias`
- `aliases`
- `conversion`

Allowed `family` values in the production catalog are:

- `base`
- `geometry`
- `mechanical`
- `electromagnetic`

## Naming Rules Captured By The Catalog

The catalog deliberately separates naming layers:

- `unit_symbol` is the human-readable wire/display symbol such as `mm`, `ft`,
  `C`, or `F`.
- `unit_code_id` is the code-safe unit id such as `mm`, `ft`, `degC`, or
  `degF`.
- `binary_unit_id` is the schema-safe wire id such as `distance.mm` or
  `temperature.degC`.
- `abi.abi_name_stem` is the dimension-level input to ABI type/function naming.

This allows the required distinctions:

- `mm` versus `Mm`
- `C` versus `degC`
- `F` versus `degF`

## Conversion Rules

The catalog conversion object supports both required forms:

- `linear`
- `affine`

Linear conversions use:

- `scale_to_base`

Affine conversions use:

- `scale_to_base`
- `offset_to_base`

Reference mapping:

- `measurement-units.csv:slope` maps to `conversion.scale_to_base`
- `measurement-units.csv:offset` maps to `conversion.offset_to_base`
- missing or zero offset becomes `null` for linear conversions

## JSON Classification Rules

The catalog owns machine-readable JSON classification through `json_forms`:

- `scalar_type_ids`
- `small_array_type_id_template`
- `buffer_type_id_template`
- `default_encoding`

Phase A decisions:

- scalars use explicit `type` + `unit` + `value`
- fixed small buffers use JSON arrays
- arbitrary/large buffers use encoded envelopes
- the chosen form is catalog-owned metadata, not a runtime heuristic

## First Generated Artifacts This Contract Must Own

Phase A and immediate follow-on generation work should derive at least:

- Rust dimension/unit registry inputs
- conversion table inputs for linear and affine conversions
- JSON type-id inventory
- ABI naming registry inputs
- downstream fixture/model generation inputs

## End-User Extension Workflow

The intended low-friction path for adding units is:

1. Edit the JSON master catalog.
2. Add or update the unit entry under the target dimension.
3. Regenerate catalog-owned artifacts.
4. Run `just test`.
5. Review the generated diff and commit both catalog and generated outputs.

Broad manual edits across Rust, Python, C#, and fixture code are not part of
the intended steady-state workflow.
