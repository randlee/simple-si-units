# Sprint B-4: Array And Buffer Quantity Model

## Goal

Implement quantity wrappers for arrays, vectors, slices, and other bulk payload forms.

## Status

`Not Started`

## Scope References

- REQ-UX-003
- REQ-UX-004
- REQ-UX-009
- REQ-UX-017
- REQ-UX-021
- REQ-UX-029
- NFR-UX-002
- NFR-UX-003
- NFR-UX-004
- NFR-UX-013
- ADR-UX-004
- ADR-UX-012
- ADR-UX-011

## Deliverables

1. Array-backed quantity forms
2. Vector-backed quantity forms
3. Borrowed slice views for the planned Rust bulk surface
4. Rules for buffer-safe storage and metadata ownership
5. Catalog-metadata-backed classification checks for small-array versus
   variable-buffer forms

## Dependencies

- Sprint A-6
- Sprint B-1

## Unblocks

- Sprints C-2, D-1, D-2, D-3, E-2, F-2

## Parallelism

- Can run in parallel with Sprint B-3

## Acceptance Criteria

1. Array-backed, vector-backed, and borrowed buffer-backed quantity forms are explicitly modeled.
2. Bulk wrappers add no per-element unit-wrapper overhead.
3. Buffer metadata ownership rules are explicit for owned and borrowed forms.
4. The resulting surface defines the bulk storage shapes, ownership rules, and
   classification inputs needed by later serialization and FFI phases without
   reopening Phase B storage decisions.
5. Bulk wrapper categories align with the catalog-owned JSON/binary
   classification metadata rather than ad hoc runtime conventions.

## Required Validation

1. Dedicated tests cover zero-length buffers.
2. Dedicated tests cover borrowed slice views and owned array-backed forms separately.
3. Size/layout assertions prove no per-element wrapper overhead.
4. Validation checks that fixed-size and variable-length bulk forms align with
   the catalog classification consumed later by serialization and interop work.

## Code Samples / Contracts

Representative wrapper shapes:

```rust
#[repr(transparent)]
pub struct QuantityArray<Unit, T, const N: usize> {
    pub values: [T; N],
    _unit: core::marker::PhantomData<Unit>,
}

pub struct QuantityVec<Unit, T> {
    pub values: Vec<T>,
    _unit: core::marker::PhantomData<Unit>,
}

pub struct QuantitySlice<'a, Unit, T> {
    pub values: &'a [T],
    _unit: core::marker::PhantomData<Unit>,
}
```
