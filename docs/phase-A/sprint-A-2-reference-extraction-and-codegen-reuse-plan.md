# Sprint A-2: Master Catalog And Codegen Reuse Plan

## Goal

Define the master catalog and isolate what can be reused from the existing project as generation inputs for the new crate.

## Status

`Done`

## Scope References

- REQ-UX-006
- REQ-UX-009
- REQ-UX-010
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

## Deliverables

1. Mapping from current CSV unit definitions to the new crate model
2. Mapping from current conversion-factor generation to the new storage-preserving model
3. Master catalog schema
4. Catalog fields covering JSON type ids, human-readable unit symbols, code-facing unit ids, binary schema ids, ABI naming inputs, reserved-word strategy, and offset-conversion metadata
5. List of codegen components to reuse, adapt, or replace
6. End-user extension workflow based on catalog edits plus regeneration
7. Authoritative in-scope type inventory for `base`, `geometry`, `mechanical`, and `electromagnetic`

## Why

The current project contains valuable unit metadata and operator relationships, but its storage model is not the new product model. The new architecture should promote the catalog itself to the primary source of truth.

## Dependencies

- Sprint A-1

## Unblocks

- Sprint B-2
- Sprint B-3
- Sprint C-1
- Sprint C-2

## Parallelism

- Can run in parallel with Sprint A-4 after Sprint A-1

## Acceptance Criteria

1. The master catalog schema is explicit enough to describe units, symbols, ids, conversion metadata, JSON classification metadata, and ABI naming inputs.
2. Every reusable input from the reference project is classified as `reuse`, `adapt`, or `replace`.
3. The extension workflow for adding a unit is documented as catalog edit plus regeneration, not broad manual edits.
4. The plan names the first generated artifacts this catalog will own.
5. The in-scope type inventory is explicit enough that later implementation sprints can check off every required public type without inference.

## Required Validation

1. A sample catalog entry exists for at least one distance unit and one temperature unit.
2. The documented schema can represent both `mm` and `Mm` distinctly.
3. The documented schema can represent `C`/`degC` style symbol-vs-code-id separation.
4. The authoritative inventory explicitly lists every in-scope reference type from `base`, `geometry`, `mechanical`, and `electromagnetic`.

## Code Samples / Contracts

Representative catalog shape:

```json
{
  "dimension": "temperature",
  "unit_code_id": "degC",
  "unit_symbol": "C",
  "reserved_word_alias": null,
  "binary_unit_id": "temperature.degC",
  "json_type_id": "temperature_f32",
  "conversion": {
    "kind": "affine",
    "scale_to_base": 1.0,
    "offset_to_base": 273.15
  }
}
```
