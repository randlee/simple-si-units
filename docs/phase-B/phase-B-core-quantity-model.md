# Phase B: Core Quantity Model

## Goal

Implement the unit-preserving storage model, conversion rules, arithmetic semantics, and array/buffer model.

## Status

`Not Started`

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

1. Unit-preserving scalar types exist.
2. Array and buffer quantity wrappers exist.
3. Conversions and arithmetic semantics are implemented.
4. Canonical compute bridges exist for derivative calculations.
