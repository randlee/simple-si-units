# Sprint A-3: ABI And Unit Naming Contract

## Goal

Lock the fundamental naming, layout, and ABI rules for the project.

## Status

`In Progress`

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

## Locked Rules

### Naming

1. ABI scalar type names use `<dimension>_<unit_code_id>_<storage>`.
2. ABI immutable slice type names use `<abi_scalar_type>_slice`.
3. ABI mutable slice type names use `<abi_scalar_type>_slice_mut`.
4. ABI scalar payload fields use `value_<unit_code_id>` for monomorphic scalar wrappers.
5. Code-safe unit marker ids preserve meaningful case distinctions, including `mm` versus `Mm`.
6. Human-readable wire/display symbols remain separate from code ids, so `degC` maps to symbol `C` and `degF` maps to symbol `F`.

### Layout

1. Stable ABI slices use `u64` for `len`.
2. `ptr == null && len == 0` is the only valid empty-slice representation.
3. `ptr == null && len > 0` is rejected.
4. Mutable and immutable slice contracts are separate concrete types.

### Ownership And Error Boundaries

1. Borrowed inputs use pointer-plus-length view structs and do not transfer ownership.
2. APIs that require caller-provided outputs must reject null output pointers explicitly with `UNITS_X_STATUS_OWNED_OUTPUT_REQUIRED`.
3. Any API that returns Rust-owned memory must surface an explicit ownership shape with enough deallocation metadata for foreign callers to pass that object back unchanged.
4. The destroy function policy is ABI-layer-specific and does not imply anything about the binary wire format.

### ABI vs Wire Format

1. `#[repr(C)]` scalar and slice structs are in-memory ABI contracts only.
2. Binary envelopes carry serialized metadata and payload bytes and are specified independently.
3. Shared naming inputs may be catalog-derived across both layers, but the layouts are not interchangeable.

## Required Validation

1. The chosen ABI examples compile as valid Rust signatures in the final design direction.
2. At least one scalar ABI example, one slice ABI example, and one status/error example are written in the doc.
3. Dedicated review confirms the naming rules distinguish human-readable symbols from code-safe identifiers.
4. The documented ABI contract states the `null ptr + zero len` behavior and the destroy-function policy for owned outputs.

## Compile-Checked Reference

The repository carries a compile-checked placeholder contract module at:

- `crates/units-x/src/ffi_contract.rs`

That module exists to prove the current Phase A naming and signature direction compiles before implementation sprints generate the real ABI surface.

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

#[repr(u32)]
pub enum units_x_status {
    UNITS_X_STATUS_OK = 0,
    UNITS_X_STATUS_NULL_WITH_LENGTH = 1,
    UNITS_X_STATUS_LOSSY_CONVERSION = 2,
    UNITS_X_STATUS_OWNED_OUTPUT_REQUIRED = 3,
    UNITS_X_STATUS_INVALID_OWNED_BUFFER = 4,
}

#[repr(C)]
pub struct units_x_owned_bytes {
    pub ptr: *mut core::ffi::c_void,
    pub len_bytes: u64,
    pub capacity_bytes: u64,
}

impl distance_mm_i32_slice {
    pub const fn is_contract_valid(self) -> bool {
        self.ptr.is_null() == (self.len == 0)
    }
}

#[unsafe(no_mangle)]
pub unsafe extern "C" fn units_x_distance_mm_i32_slice_sum(
    input: distance_mm_i32_slice,
    out: *mut distance_mm_i32,
) -> units_x_status {
    if !input.is_contract_valid() {
        return units_x_status::UNITS_X_STATUS_NULL_WITH_LENGTH;
    }
    if out.is_null() {
        return units_x_status::UNITS_X_STATUS_OWNED_OUTPUT_REQUIRED;
    }
    units_x_status::UNITS_X_STATUS_OK
}

#[unsafe(no_mangle)]
pub unsafe extern "C" fn units_x_owned_buffer_destroy(
    buffer: units_x_owned_bytes,
) -> units_x_status {
    if buffer.ptr.is_null() {
        return if buffer.len_bytes == 0 && buffer.capacity_bytes == 0 {
            units_x_status::UNITS_X_STATUS_OK
        } else {
            units_x_status::UNITS_X_STATUS_NULL_WITH_LENGTH
        };
    }
    if buffer.capacity_bytes < buffer.len_bytes {
        return units_x_status::UNITS_X_STATUS_INVALID_OWNED_BUFFER;
    }
    units_x_status::UNITS_X_STATUS_OK
}

pub struct mm;
pub struct Mm;
pub struct degC;
pub struct degF;
```

Contract note:

- `ptr == null && len == 0` is the only valid empty-slice representation.
- `ptr == null && len > 0` is rejected.
- `out == null` is rejected with `UNITS_X_STATUS_OWNED_OUTPUT_REQUIRED`.
- Rust-owned output buffers use `units_x_owned_bytes`, and both `len_bytes` and `capacity_bytes` are byte counts.
- binary wire envelopes remain a separate serialized contract and are not ABI structs.
