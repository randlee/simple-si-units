# Sprint D-1: Stable C ABI Types And Exported Functions

## Goal

Implement the concrete exported ABI layer for scalars and slices.

## Status

`Not Started`

## Deliverables

1. Concrete scalar ABI structs
2. Slice and mutable-slice ABI structs
3. Explicit exported conversion and compute functions
4. Header or ABI documentation generation path

## Dependencies

- Sprints B-3, B-4, C-2

## Unblocks

- Sprints D-2, D-3
- Python low-level buffer work where applicable

## Exit Criteria

1. ABI structs are concrete, stable, and tested for layout.
2. Exported functions are explicit and FFI-safe.
