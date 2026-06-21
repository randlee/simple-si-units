# Phase B: Core Quantity Model

## Goal

Implement the unit-preserving storage model, conversion rules, arithmetic semantics, and array/buffer model.

## Status

`Not Started`

## Scope References

- REQ-UX-001
- REQ-UX-002
- REQ-UX-003
- REQ-UX-006
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
- REQ-UX-035
- NFR-UX-001
- NFR-UX-002
- ADR-UX-002
- ADR-UX-020
- ADR-UX-013
- ADR-UX-021

## Phase Dependencies

- [Phase A](../phase-A/phase-A-foundation-and-deliverable-bootstrap.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint B-1](sprint-B-1-core-storage-types-and-unit-markers.md) | Core storage types and unit markers | Phase A | None | `Not Started` |
| [Sprint B-2](sprint-B-2-unit-conversions-and-temperature-offsets.md) | Multiplicative conversions plus Celsius/Fahrenheit support | Sprints A-2, A-3, B-1 | None | `Not Started` |
| [Sprint B-3](sprint-B-3-arithmetic-semantics-and-canonical-compute-bridges.md) | Arithmetic semantics and canonical compute bridges | Sprints A-2, A-3, B-1 | Sprint B-4 | `Not Started` |
| [Sprint B-4](sprint-B-4-array-and-buffer-quantity-model.md) | Array and buffer quantity model | Sprints A-3, B-1 | Sprint B-3 | `Not Started` |

## Phase Completion Criteria

Phase B is complete when:

1. Unit-preserving scalar types exist for every item in
   [docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md).
2. Array and buffer quantity wrappers exist.
3. Conversions are implemented across the in-scope families, including domain-important reciprocal units such as `Diopter`.
4. Arithmetic semantics and canonical compute bridges are implemented for the documented derived-operation set.
