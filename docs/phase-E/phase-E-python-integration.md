# Phase E: Python Integration

## Goal

Build the Python-facing API under `python/` using PyO3/maturin, with scalar ergonomics and buffer-oriented bulk data.

## Status

`Not Started`

## Scope References

- REQ-ROOT-014
- REQ-ROOT-016
- REQ-ROOT-017
- REQ-UX-012
- REQ-UX-015
- REQ-UX-016
- REQ-UX-030
- REQ-UX-031
- REQ-UX-032
- REQ-UX-033
- REQ-UX-040
- NFR-UX-007
- NFR-UX-011
- NFR-UX-012
- NFR-UX-013
- ADR-ROOT-007
- ADR-UX-004
- ADR-UX-014

## Phase Dependencies

- [Phase B](../phase-B/phase-B-core-quantity-model.md)
- [Phase C](../phase-C/phase-C-serialization-and-binary-contract.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint E-1](sprint-E-1-pyo3-maturin-scalar-api.md) | PyO3/maturin scalar API | Sprints B-2, B-3, C-1, C-3 | None | `Not Started` |
| [Sprint E-2](sprint-E-2-python-buffer-and-memoryview-api.md) | Python buffer and memoryview API | Sprints B-4, C-2, C-3 | None | `Not Started` |
| [Sprint E-3](sprint-E-3-python-tests-and-pydantic-models.md) | Python tests and generated Pydantic models | Sprints A-5, E-1, E-2 | Sprint E-4 | `Not Started` |
| [Sprint E-4](sprint-E-4-python-packaging-and-examples.md) | Python packaging, install flow, and examples | Sprint E-3 | None | `Not Started` |

## Phase Completion Criteria

Phase E is complete when:

1. Python scalar APIs cover the shipped scalar public surface without omission.
2. Python array and buffer APIs avoid per-element object overhead and document owned, borrowed, read-only, and mutable semantics explicitly.
3. Generated Pydantic models exist for every canonical JSON type shipped by the project.
4. Packaging, built-artifact install flow, and examples are validated with `maturin` against the same canonical fixtures used by Rust and C#.
5. The Python package is ready for `pip install` and version-synchronized with the shared project version source with no implicit deferrals of shipped scalar or bulk surfaces.
