# Sprint D-1: Stable C ABI Types And Exported Functions

## Goal

Implement the concrete exported ABI layer for scalars and slices.

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

1. Concrete scalar ABI structs
2. Slice and mutable-slice ABI structs
3. Explicit exported conversion and compute functions
4. Header or ABI documentation generation path
5. Explicit ABI status/error model for slice and buffer operations
6. Explicit ownership and destroy-function policy for any non-trivial ABI resources

## Dependencies

- Sprints A-3, B-2, B-3, B-4, C-2, C-3

## Unblocks

- Sprints D-2, D-3
- Python low-level FFI work if the Python surface intentionally reuses the C ABI layer

## Acceptance Criteria

1. Concrete scalar ABI structs are defined for the initial shipped surface.
2. Slice and mutable-slice ABI structs are defined with the chosen `u64` length contract.
3. Exported conversion and compute functions are explicit rather than trait- or operator-driven.
4. ABI error/status behavior is explicit for failing slice/buffer operations.
5. Ownership and destroy-function rules are explicit for any non-trivial resources.

## Required Validation

1. Layout tests cover every exported scalar and slice struct.
2. Dedicated tests cover `null ptr + non-zero len` rejection.
3. Dedicated tests cover `null ptr + zero len` behavior according to the chosen contract.
4. Exported header or ABI documentation generation is reproducible from repo tooling.
5. Dedicated tests or review checks cover any destroy-function contract that reaches the shipped surface.

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

pub extern "C" fn units_x_owned_buffer_destroy(
    ptr: *mut core::ffi::c_void,
    len: u64,
) -> units_x_status;
```
