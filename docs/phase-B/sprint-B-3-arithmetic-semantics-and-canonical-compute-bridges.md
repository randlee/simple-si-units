# Sprint B-3: Arithmetic Semantics And Canonical Compute Bridges

## Goal

Define and implement scalar arithmetic, mixed-unit addition/subtraction, and bridges to canonical compute outputs for derived calculations.

## Status

`Not Started`

## Deliverables

1. Scalar multiplication and division preserving declared unit
2. Mixed-unit addition and subtraction with left-hand-unit preservation
3. Deterministic mixed-storage promotion rules
4. Canonical compute bridges for velocity and acceleration calculations

## Dependencies

- Sprints A-2, A-3, B-1

## Unblocks

- Sprints D-1, E-1, F-1

## Parallelism

- Can run in parallel with Sprint B-4 after B-1

## Exit Criteria

1. Arithmetic behavior matches the PRD.
2. Derived calculations are limited to the documented canonical set rather than exposing undocumented combinatorial result types.
3. Mixed-storage behavior is deterministic and documented.
