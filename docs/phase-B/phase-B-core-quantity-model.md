# Phase B: Core Quantity Model

## Goal

Implement the unit-preserving storage model, catalog-owned conversion rules,
canonical-dimension arithmetic semantics, and array/buffer model.

## Status

`In Progress`

## Scope References

- REQ-UX-001
- REQ-UX-002
- REQ-UX-003
- REQ-UX-004
- REQ-UX-006
- REQ-UX-009
- REQ-UX-008
- REQ-UX-011
- REQ-UX-023
- REQ-UX-024
- REQ-UX-025
- REQ-UX-026
- REQ-UX-027
- REQ-UX-028
- REQ-UX-042
- REQ-UX-043
- REQ-UX-044
- REQ-UX-045
- REQ-UX-046
- REQ-UX-029
- REQ-UX-034
- REQ-UX-040
- REQ-UX-035
- NFR-UX-001
- NFR-UX-002
- NFR-UX-013
- ADR-UX-002
- ADR-UX-003
- ADR-UX-017
- ADR-UX-022
- ADR-UX-020
- ADR-UX-012
- ADR-UX-013
- ADR-UX-021

## Phase Dependencies

- [Phase A](../phase-A/phase-A-foundation-and-deliverable-bootstrap.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint B-1](sprint-B-1-core-storage-types-and-unit-markers.md) | Core storage types and unit markers | Sprint A-6 | None | `Complete` |
| [Sprint B-2](sprint-B-2-unit-conversions-and-temperature-offsets.md) | Catalog-owned conversions plus Celsius/Fahrenheit support | Sprint A-6, Sprint B-1 | None | `Not Started` |
| [Sprint B-3](sprint-B-3-arithmetic-semantics-and-canonical-compute-bridges.md) | Arithmetic semantics and canonical compute bridges | Sprint A-6, Sprint B-1, Sprint B-2 | Sprint B-4 | `Not Started` |
| [Sprint B-4](sprint-B-4-array-and-buffer-quantity-model.md) | Array and buffer quantity model | Sprint A-6, Sprint B-1 | Sprint B-3 | `Not Started` |

## Phase Completion Criteria

Phase B is complete when:

1. Unit-preserving scalar types exist for every item in
   [docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md).
2. Implemented scalar, array, and buffer surfaces match catalog-derived
   metadata and regenerate cleanly from the authoritative catalog.
3. Conversions are implemented from catalog-owned conversion metadata across
   the in-scope families, including domain-important reciprocal units such as
   `Diopter`.
4. Arithmetic semantics use catalog `canonical_dimension_id` to determine
   same-dimension compatibility and canonical compute bridge eligibility.
5. Inventory-backed validation demonstrates closure for every in-scope type
   rather than representative-family sampling.
