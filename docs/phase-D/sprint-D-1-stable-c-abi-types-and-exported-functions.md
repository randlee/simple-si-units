# Sprint D-1: Stable C ABI Types And Exported Functions

## Goal

Implement the concrete exported ABI layer for scalars, slices, owned buffers,
and explicit conversion and compute functions.

## Status

`Not Started`

## Scope References

- REQ-UX-019
- REQ-UX-020
- REQ-UX-021
- REQ-UX-022
- REQ-UX-037
- REQ-UX-038
- REQ-UX-040
- NFR-UX-003
- NFR-UX-004
- NFR-UX-007
- ADR-UX-004
- ADR-UX-005
- ADR-UX-017
- ADR-UX-011

## Deliverables

1. Concrete scalar ABI structs for every shipped scalar ABI contract row
2. Slice and mutable-slice ABI structs plus any shipped owned-buffer ABI structs
3. Explicit exported conversion and compute functions for every shipped ABI operation
4. Header or ABI documentation generation path
5. Explicit ABI status/error model for slice and buffer operations
6. Explicit ownership and destroy-function policy for any non-trivial ABI resources
7. Generated ABI inventory artifact mapping catalog/public types to exported ABI rows

## Dependencies

- Sprints A-3, B-2, B-3, B-4, C-2, C-3

## Unblocks

- Sprints D-2, D-3
- Optional low-level Python FFI reuse work if Phase E intentionally consumes the
  stable C ABI beneath its higher-level PyO3 surface

## Acceptance Criteria

1. Concrete scalar ABI structs are defined for every shipped scalar ABI contract row.
2. Slice, mutable-slice, and owned-buffer ABI structs are defined with the chosen `u64` length contract wherever those shape classes are shipped.
3. Exported conversion and compute functions are explicit rather than trait- or operator-driven.
4. ABI error/status behavior is explicit for failing slice and buffer operations.
5. Ownership and destroy-function rules are explicit for every non-trivial resource that reaches the shipped surface.
6. The sprint closure artifact records every shipped ABI row and shows no omitted shape classes.

## Required Validation

1. Layout tests cover every exported scalar, slice, mutable-slice, and owned-buffer struct that reaches the shipped surface.
2. Dedicated tests cover `null ptr + non-zero len` rejection.
3. Dedicated tests cover `null ptr + zero len` behavior according to the chosen contract.
4. Exported header or ABI documentation generation is reproducible from repo tooling.
5. Dedicated tests or review checks cover every destroy-function contract that reaches the shipped surface.

## ABI Boundary Rule

This sprint closes the stable C ABI only. It does not redefine the canonical
JSON DTO contract or the binary envelope schema from Phase C. Exported rows are
monomorphic, catalog-derived, and named deterministically according to the
architecture ADRs. The sprint does not close on representative coverage; every
shipped ABI row must be accounted for in the generated inventory artifact.

## Code Samples / Contracts

```rust
#[repr(C)]
pub struct distance_m_f64 {
    pub value_m: f64,
}

#[repr(C)]
pub struct distance_m_f64_slice {
    pub ptr: *const distance_m_f64,
    pub len: u64,
}

#[repr(C)]
pub enum units_x_status {
    UNITS_X_STATUS_OK = 0,
    UNITS_X_STATUS_NULL_WITH_LENGTH = 1,
    UNITS_X_STATUS_LOSSY_CONVERSION = 2,
}

pub extern "C" fn units_x_distance_m_f64_to_ft(
    input: distance_m_f64,
    out: *mut distance_ft_f64,
) -> units_x_status;

#[repr(C)]
pub struct units_x_owned_bytes {
    pub ptr: *mut core::ffi::c_void,
    pub len: u64,
}

pub extern "C" fn units_x_owned_buffer_destroy(
    buffer: units_x_owned_bytes,
) -> units_x_status;
```
