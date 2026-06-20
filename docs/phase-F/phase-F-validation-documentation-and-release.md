# Phase F: Validation, Documentation, And Release

## Goal

Validate parity, confirm storage and ABI goals, finish cross-language examples, verify shared-version locking, and prepare the project for initial release.

## Status

`Not Started`

## Phase Dependencies

- [Phase D](../phase-D/phase-D-interop-surfaces.md)
- [Phase E](../phase-E/phase-E-python-integration.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint F-1](sprint-F-1-reference-parity-and-correctness-suite.md) | Reference parity and correctness suite | Sprints B-3, C-1 | Sprint F-2 | `Not Started` |
| [Sprint F-2](sprint-F-2-footprint-layout-and-performance-validation.md) | Footprint, layout, and performance validation | Sprints B-4, C-3, D-1 | Sprint F-1 | `Not Started` |
| [Sprint F-3](sprint-F-3-user-documentation-examples-and-release-readiness.md) | User docs, examples, packaging, and release readiness | Phases D-E, Sprints F-1-F-2 | None | `Not Started` |

## Phase Completion Criteria

Phase F is complete when:

1. Correctness is validated against the reference implementation where appropriate.
2. Size, ABI, and footprint claims are test-backed.
3. Consumer-facing docs and examples are ready for first release.
4. crates.io, PyPI/pip, and NuGet release readiness plus version synchronization are validated.
