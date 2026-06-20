# Sprint B-4: Array And Buffer Quantity Model

## Goal

Implement quantity wrappers for arrays, vectors, slices, and other bulk payload forms.

## Status

`Not Started`

## Deliverables

1. Array-backed quantity forms
2. Vector-backed quantity forms
3. Borrowed slice views where appropriate
4. Rules for buffer-safe storage and metadata ownership

## Dependencies

- Sprints A-3, B-1

## Unblocks

- Sprints C-2, D-1, D-2, D-3, E-2, F-2

## Parallelism

- Can run in parallel with Sprint B-3

## Exit Criteria

1. Bulk quantity wrappers add no per-element overhead.
2. Buffer-oriented APIs are ready for serialization and FFI work.
