# Phase E: Python Integration

## Goal

Build the Python-facing API under `python/` using PyO3/maturin, with scalar ergonomics and buffer-oriented bulk data.

## Status

`Not Started`

## Phase Dependencies

- [Phase B](../phase-B/phase-B-core-quantity-model.md)
- [Phase C](../phase-C/phase-C-serialization-and-binary-contract.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint E-1](sprint-E-1-pyo3-maturin-scalar-api.md) | PyO3/maturin scalar API | Sprints B-2, B-3, C-1 | None | `Not Started` |
| [Sprint E-2](sprint-E-2-python-buffer-and-memoryview-api.md) | Python buffer and memoryview API | Sprints B-4, C-2 | None | `Not Started` |
| [Sprint E-3](sprint-E-3-python-tests-packaging-and-examples.md) | Python tests, packaging, and examples | Sprints E-1, E-2 | None | `Not Started` |

## Phase Completion Criteria

Phase E is complete when:

1. Python scalar APIs are ergonomic.
2. Python array/buffer APIs avoid per-element object overhead.
3. Generated Pydantic models exist for all public JSON types.
4. Packaging and examples are validated with `maturin`.
5. The Python package is ready for `pip install` and version-synchronized with the shared project version source.
