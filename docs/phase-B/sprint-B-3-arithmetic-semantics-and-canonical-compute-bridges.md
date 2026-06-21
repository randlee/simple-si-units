# Sprint B-3: Arithmetic Semantics And Canonical Compute Bridges

## Goal

Define and implement scalar arithmetic, mixed-unit addition/subtraction, and bridges to canonical compute outputs for derived calculations.

## Status

`Not Started`

## Scope References

- REQ-UX-023
- REQ-UX-024
- REQ-UX-025
- REQ-UX-026
- REQ-UX-027
- REQ-UX-028
- REQ-UX-041
- REQ-UX-045
- ADR-UX-013
- ADR-UX-019

## Deliverables

1. Same-dimension scalar multiply-by-scalar and divide-by-scalar semantics across the authoritative inventory
2. Same-dimension mixed-unit addition and subtraction with left-hand-unit preservation across the authoritative inventory
3. Deterministic mixed-storage promotion rules
4. Canonical compute bridges for velocity and acceleration calculations
5. Explicit non-support boundary for the legacy cross-dimension operator graph beyond the documented bridge set

## Dependencies

- Sprints A-2, A-3, B-1

## Unblocks

- Sprints D-1, E-1, F-1

## Parallelism

- Can run in parallel with Sprint B-4 after B-1

## Acceptance Criteria

1. Multiplication and division by unitless scalars preserve the declared unit across the authoritative inventory.
2. Mixed-unit addition and subtraction use one documented unit-preservation rule across the authoritative inventory.
3. Mixed-storage arithmetic uses one documented promotion rule.
4. Derived calculations are limited to the documented canonical set rather than open-ended combinatorial result typing.
5. The sprint explicitly states which arithmetic is intentionally unsupported in V1 instead of leaving gaps for inference.

## Required Validation

1. Dedicated tests cover `distance_cm + distance_m` with documented left-hand preservation behavior.
2. Dedicated tests cover mixed integer/float storage promotion.
3. Dedicated tests cover the distance -> velocity -> acceleration chain.
4. Dedicated tests cover zero-duration rejection or failure behavior for velocity/acceleration compute bridges.
5. Validation covers at least one same-dimension arithmetic case from `base`, `geometry`, `mechanical`, `electromagnetic`, and `Diopter`.

## Code Samples / Contracts

Representative semantics:

```rust
let lhs = Distance::cm(25.0);
let rhs = Distance::m(1.0);
let out = lhs + rhs;
assert_eq!(out.unit(), "cm");

let scaled = out * 2.0;
assert_eq!(scaled.unit(), "cm");
```

V1 non-support boundary:

- this sprint does not promise reconstruction of the full legacy cross-dimension operator graph
- unsupported cross-dimension combinations must be documented as intentionally out of scope rather than silently omitted
