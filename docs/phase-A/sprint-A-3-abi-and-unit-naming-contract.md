# Sprint A-3: ABI And Unit Naming Contract

## Goal

Lock the fundamental naming, layout, and ABI rules for the project.

## Status

`Not Started`

## Scope References

- REQ-UX-010
- REQ-UX-018
- REQ-UX-019
- REQ-UX-020
- REQ-UX-021
- REQ-UX-022
- REQ-UX-037
- REQ-UX-038
- REQ-UX-040
- NFR-UX-003
- NFR-UX-004
- ADR-UX-004
- ADR-UX-005
- ADR-UX-010
- ADR-UX-011
- ADR-UX-017

## Deliverables

1. Concrete rule for ABI-facing struct naming
2. Concrete rule for type-level unit marker naming and symbol casing
3. Concrete rule for slice layout and length width
4. Concrete rule for FFI-safe ownership boundaries
5. Concrete rule distinguishing in-memory ABI layout from binary wire format

## Why

This project depends on stable, cross-language behavior. Naming and layout rules must be frozen before code generation and wrapper generation.

## Dependencies

- Sprint A-1

## Unblocks

- Sprint B-1
- Sprint C-2
- Sprint D-1
- Sprint D-2
- Sprint D-3

## Parallelism

- Can run in parallel with Sprint A-4 after Sprint A-1

## Acceptance Criteria

1. Public ABI naming rules are explicit for scalar, slice, and mutable-slice types.
2. Unit marker casing and code-id rules cover `mm`, `Mm`, `degC`, and `degF`.
3. The `u64` ABI slice length contract is chosen and documented.
4. ABI ownership and error-reporting boundaries are explicit enough for downstream bindings to rely on without inference.
5. In-memory ABI layout and binary wire format are documented as separate contracts.

## Required Validation

1. The chosen ABI examples compile as valid Rust signatures in the final design direction.
2. At least one scalar ABI example, one slice ABI example, and one status/error example are written in the doc.
3. Dedicated review confirms the naming rules distinguish human-readable symbols from code-safe identifiers.
4. The documented ABI contract states the `null ptr + zero len` behavior and the destroy-function policy for owned outputs.

## Code Samples / Contracts

Representative ABI shape:

```rust
#[repr(C)]
pub struct distance_mm_i32 {
    pub value_mm: i32,
}

#[repr(C)]
pub struct distance_mm_i32_slice {
    pub ptr: *const distance_mm_i32,
    pub len: u64,
}

#[repr(C)]
pub enum units_x_status {
    UNITS_X_STATUS_OK = 0,
    UNITS_X_STATUS_NULL_WITH_LENGTH = 1,
    UNITS_X_STATUS_LOSSY_CONVERSION = 2,
}

pub extern "C" fn units_x_distance_mm_i32_slice_sum(
    input: distance_mm_i32_slice,
    out: *mut distance_mm_i32,
) -> units_x_status;

pub extern "C" fn units_x_owned_buffer_destroy(
    ptr: *mut core::ffi::c_void,
    len: u64,
) -> units_x_status;

pub struct mm;
pub struct Mm;
pub struct degC;
```

Contract note:

- `ptr == null && len == 0` is the only valid empty-slice representation.
- `ptr == null && len > 0` is rejected.
- binary wire envelopes remain a separate serialized contract and are not ABI structs.
