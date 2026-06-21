# Sprint A-6: Phase-End Fixes

## Goal

Close the remaining Phase A blockers so the catalog and generated metadata match
the documented MVP inventory and reciprocal-domain contract.

## Status

`Done`

## Scope References

- REQ-ROOT-010
- REQ-ROOT-011
- REQ-ROOT-020
- REQ-UX-029
- REQ-UX-032
- REQ-UX-034
- REQ-UX-035
- REQ-UX-040
- REQ-UX-042
- REQ-UX-043
- REQ-UX-044
- NFR-UX-013
- ADR-UX-012
- ADR-UX-015
- ADR-UX-017
- ADR-UX-020

## Dependencies

- Sprint A-5
- [phase-A-findings-1.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-findings-1.md)

## Deliverables

1. Production catalog expanded to the full authoritative MVP public type inventory.
2. Catalog/schema support for public quantities that map to a canonical underlying dimension.
3. `Diopter` remodeled as a first-class public type mapped to `InverseDistance`.
4. Generated catalog summary and Rust metadata regenerated from the corrected catalog.
5. Regression tests that compare generated catalog coverage against the authoritative inventory and assert the `Diopter -> inverse_distance` mapping.

## Acceptance Criteria

1. `catalog/units-catalog.json` contains one row for every public type listed in
   [docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md).
2. Every catalog row declares `canonical_dimension_id`, and validation rejects references to unknown canonical dimensions.
3. Generated metadata exposes the canonical-dimension mapping so downstream Rust/C#/Python generation can consume it without inferring physics from names.
4. `Diopter` keeps its public namespace and wire id while declaring
   `canonical_dimension_id: "inverse_distance"`.
5. `just test` passes from a clean checkout after regeneration.

## Required Validation

1. Catalog contract validation covers canonical-dimension ids and rejects broken mappings.
2. Generation tests assert that the generated summary public types exactly match the authoritative inventory checklist.
3. Rust tests assert that generated metadata contains a `Diopter` entry whose canonical dimension is `inverse_distance`.
4. Regeneration from a clean checkout reproduces the committed generated artifacts.
