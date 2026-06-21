# Sprint F-1: Reference Parity And Correctness Suite

## Goal

Validate correctness against the existing project for operations that both the
reference crates and `units-x` implement, and add direct contract tests for new
`units-x`-only behavior.

## Status

`Not Started`

## Scope References

- REQ-UX-006
- REQ-UX-008
- REQ-UX-023
- REQ-UX-024
- REQ-UX-032
- REQ-UX-042
- REQ-UX-043
- REQ-UX-044
- ADR-UX-003
- ADR-UX-014
- ADR-UX-021

## Deliverables

1. Conversion parity tests across the in-scope unit families
2. Canonical compute parity tests
3. Temperature conversion correctness tests
4. Reciprocal-domain correctness tests including `Diopter`
5. Catalog-driven generated test coverage for declared units
6. Final parity completion for every item in
   [docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md)

## Dependencies

- Sprints A-2, A-5, B-2, B-3, C-1

## Unblocks

- Sprint F-3

## Parallelism

- Can run in parallel with Sprint F-2

## Acceptance Criteria

1. Conversion and canonical-compute correctness claims are backed by executable parity tests for behaviors shared with the reference crates.
2. Temperature conversions have dedicated correctness coverage.
3. Domain-reciprocal public units such as `Diopter` have dedicated correctness coverage.
4. Declared units in the catalog are covered by generated or catalog-driven tests.
5. The final parity checklist shows no unreviewed omission for any in-scope public type.

## Required Validation

1. Dedicated parity tests cover representative `base`, `geometry`, `mechanical`, and `electromagnetic` quantities plus temperature conversions.
2. Dedicated tests compare derivative compute results when both the reference crates and `units-x` implement the same derivative contract, and otherwise assert the `units-x` contract directly.
3. Dedicated tests cover `Diopter` correctness against the reciprocal-distance contract.
4. Validation explicitly records the test or rationale path for every item in
   the authoritative inventory.

## Parity Checklist

The authoritative checklist for this sprint is
[docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md).
This sprint does not close until every item in that checklist has an explicit
parity or contract-test path recorded.
