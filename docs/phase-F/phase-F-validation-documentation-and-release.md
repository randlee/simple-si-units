# Phase F: Validation, Documentation, And Release

## Goal

Validate parity, confirm storage and ABI goals, finish cross-language examples, verify shared-version locking, and prepare the project for initial release.

## Status

`Not Started`

## Scope References

- REQ-ROOT-010
- REQ-ROOT-011
- REQ-ROOT-014
- REQ-ROOT-015
- REQ-UX-006
- REQ-UX-023
- REQ-UX-032
- REQ-UX-033
- REQ-UX-042
- REQ-UX-043
- REQ-UX-044
- NFR-UX-001
- NFR-UX-003
- NFR-UX-005
- NFR-UX-011
- NFR-UX-012
- ADR-UX-006
- ADR-UX-014
- ADR-UX-020
- ADR-UX-021

## Phase Dependencies

- [Phase D](../phase-D/phase-D-interop-surfaces.md)
- [Phase E](../phase-E/phase-E-python-integration.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint F-1](sprint-F-1-reference-parity-and-correctness-suite.md) | Reference parity and correctness suite | Sprints A-5, B-2, B-3, C-1 | Sprint F-2 | `Not Started` |
| [Sprint F-2](sprint-F-2-footprint-layout-and-performance-validation.md) | Footprint, layout, and performance validation | Sprints B-4, C-3, D-1 | Sprint F-1 | `Not Started` |
| [Sprint F-3](sprint-F-3-user-documentation-and-examples.md) | User docs and final cross-language examples | Phases D-E, Sprints F-1-F-2 | Sprint F-4 | `Not Started` |
| [Sprint F-4](sprint-F-4-release-readiness-and-publication-dry-run.md) | Release readiness, publication dry runs, and final version-lock signoff | Sprints F-1, F-2, F-3 | None | `Not Started` |

## Phase Completion Criteria

Phase F is complete when:

1. Correctness is validated against the reference implementation for every item in
   [docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md)
   where shared reference behavior exists, and new `units-x`-only behavior is
   covered by dedicated contract tests.
2. Size, ABI, and footprint claims are test-backed.
3. Consumer-facing docs and examples are ready for first release.
4. crates.io, PyPI/pip, and NuGet release readiness plus version synchronization are validated.
