# Sprint B-4: Array And Buffer Quantity Model

## Goal

Implement quantity wrappers for fixed arrays, owned buffers, and borrowed slice
views.

## Status

`Done`

## Scope References

- REQ-UX-003
- REQ-UX-004
- REQ-UX-009
- REQ-UX-017
- REQ-UX-029
- NFR-UX-002
- NFR-UX-003
- NFR-UX-004
- NFR-UX-013
- ADR-UX-004
- ADR-UX-012

## Deliverables

1. Fixed-size array-backed quantity forms
2. Owned variable-length buffer quantity form for the public Rust bulk surface
3. Borrowed variable-length buffer view for the public Rust bulk surface
4. Rules for buffer-safe storage and metadata ownership
5. Generated bulk-support matrix at `catalog/generated/phase-b-bulk-support.json`

## Dependencies

- Sprint A-6
- Sprint B-1

## Unblocks

- Sprints C-2, D-1, D-2, D-3, E-2, F-2

## Parallelism

- Can run in parallel with Sprint B-3

## Out Of Scope

- stable C-ABI slice structs, fixed-width ABI length fields, and exported ABI
  status models, which close in Phase D
- JSON envelopes and binary envelopes, which close in Phase C

## Acceptance Criteria

1. The authoritative public Rust bulk surface is explicitly limited to
   `QuantityArray`, `QuantityBuffer`, and `QuantityBufferView`.
2. Bulk wrappers add no per-element unit-wrapper overhead.
3. Buffer metadata ownership rules are explicit for owned and borrowed forms.
4. The resulting surface defines the bulk storage shapes, ownership rules, and
   classification inputs needed by later serialization and FFI phases without
   reopening Phase B storage decisions.
5. Bulk wrapper categories align with the catalog-owned JSON/binary
   classification metadata rather than ad hoc runtime conventions.
6. `catalog/generated/phase-b-bulk-support.json` is the authoritative closure
   artifact for fixed-array versus variable-buffer support and classification
   parity.
7. Fixed-array rows in the authoritative bulk-support artifact are uniquely
   keyed by array arity so per-array-size classification can be reviewed
   without inference.
8. The authoritative bulk-support artifact uses the review arity set
   `{0, 2, 3, 4}` in V1; the runtime `QuantityArray<Unit, T, N>` surface
   remains generic over any `N`.
9. Bulk wrappers only compile for unit/storage combinations published by the
   catalog-derived bulk-support contract; unsupported combinations are absent
   at compile time rather than synthesized ad hoc.

## Required Validation

1. Dedicated tests cover zero-length buffers.
2. Dedicated tests cover borrowed slice views and owned array-backed forms separately.
3. Size/layout assertions prove no per-element wrapper overhead.
4. Validation checks that fixed-size and variable-length bulk forms align with
   the catalog classification consumed later by serialization and interop work.
5. Validation confirms `catalog/generated/phase-b-bulk-support.json`
   enumerates every supported or intentionally unsupported bulk-classification
   row exactly once.
6. Validation confirms fixed-array rows in
   `catalog/generated/phase-b-bulk-support.json` include explicit array arity
   and map directly to the catalog `small_array` classification inputs.

## Code Samples / Contracts

Representative wrapper shapes:

```rust
#[repr(transparent)]
pub struct QuantityArray<Unit, T, const N: usize> {
    pub values: [T; N],
    _unit: core::marker::PhantomData<Unit>,
}

pub struct QuantityBuffer<Unit, T> {
    pub values: Vec<T>,
    _unit: core::marker::PhantomData<Unit>,
}

pub struct QuantityBufferView<'a, Unit, T> {
    pub values: &'a [T],
    _unit: core::marker::PhantomData<Unit>,
}
```

Authoritative bulk-boundary rule:

- `QuantityArray<Unit, T, N>` is the authoritative fixed-size public Rust bulk
  wrapper
- `QuantityBuffer<Unit, T>` is the authoritative owned variable-length public
  Rust bulk wrapper
- `QuantityBufferView<'a, Unit, T>` is the authoritative borrowed
  variable-length public Rust bulk wrapper
- a generated `BulkStorageFor<Unit>` gate constrains those wrappers to the
  storage set published for each unit family in the catalog
- `Vec<T>` and `&[T]` are payload/storage details of those wrappers, not
  competing public quantity boundary shapes

Authoritative bulk-support artifact columns:

- `public_type`
- `bulk_kind`
- `array_arity`
- `storage`
- `classification`
- `support_status`
- `expected_failure`

## Closure Gate

This sprint does not close until `catalog/generated/phase-b-bulk-support.json`
enumerates every supported or intentionally unsupported fixed-array and
variable-buffer classification row exactly once, includes explicit fixed-array
arity for `small_array` rows, and matches the catalog-owned classification
metadata consumed by later phases.
