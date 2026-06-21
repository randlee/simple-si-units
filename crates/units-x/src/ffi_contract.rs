#![allow(non_camel_case_types)]

use core::ffi::c_void;
use core::marker::PhantomData;

/// Unit marker preserving the lowercase wire/code distinction for millimeters.
pub struct mm;

/// Unit marker preserving the uppercase/lowercase distinction for megameters.
pub struct Mm;

/// Code-safe unit marker for Celsius, whose wire symbol remains `C`.
pub struct degC;

/// Code-safe unit marker for Fahrenheit, whose wire symbol remains `F`.
pub struct degF;

/// Placeholder generic quantity shape used only to pin the contract direction.
#[repr(transparent)]
pub struct quantity<Unit, Storage> {
    pub storage: Storage,
    _unit: PhantomData<Unit>,
}

/// ABI-facing scalar name pattern: `<dimension>_<unit_code_id>_<storage>`.
#[repr(C)]
#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub struct distance_mm_i32 {
    pub value_mm: i32,
}

/// ABI slice pattern: `<abi_scalar_type>_slice`.
#[repr(C)]
#[derive(Copy, Clone, Debug)]
pub struct distance_mm_i32_slice {
    pub ptr: *const distance_mm_i32,
    pub len: u64,
}

impl distance_mm_i32_slice {
    /// `null + zero` is the only valid empty-slice representation.
    pub const fn is_contract_valid(self) -> bool {
        self.ptr.is_null() == (self.len == 0)
    }
}

/// Mutable ABI slice pattern: `<abi_scalar_type>_slice_mut`.
#[repr(C)]
#[derive(Copy, Clone, Debug)]
pub struct distance_mm_i32_slice_mut {
    pub ptr: *mut distance_mm_i32,
    pub len: u64,
}

impl distance_mm_i32_slice_mut {
    /// `null + zero` is the only valid empty-slice representation.
    pub const fn is_contract_valid(self) -> bool {
        self.ptr.is_null() == (self.len == 0)
    }
}

/// Explicit Rust-owned byte-buffer contract for ABI-returned payloads.
#[repr(C)]
#[derive(Copy, Clone, Debug)]
pub struct units_x_owned_bytes {
    pub ptr: *mut c_void,
    pub len_bytes: u64,
    pub capacity_bytes: u64,
}

impl units_x_owned_bytes {
    /// Empty buffers are `null + zero + zero`; non-empty buffers use byte counts.
    pub const fn is_contract_valid(self) -> bool {
        if self.ptr.is_null() {
            self.len_bytes == 0 && self.capacity_bytes == 0
        } else {
            self.capacity_bytes >= self.len_bytes
        }
    }
}

/// Shared ABI status surface for cross-language bindings.
#[repr(u32)]
#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum units_x_status {
    UNITS_X_STATUS_OK = 0,
    UNITS_X_STATUS_NULL_WITH_LENGTH = 1,
    UNITS_X_STATUS_LOSSY_CONVERSION = 2,
    UNITS_X_STATUS_OWNED_OUTPUT_REQUIRED = 3,
    UNITS_X_STATUS_INVALID_OWNED_BUFFER = 4,
}

/// Representative scalar-returning ABI export shape.
///
/// # Safety
///
/// `out` must be either null or point to writable storage for one
/// `distance_mm_i32` value. `input` must satisfy the slice validity contract:
/// `null + zero` is allowed, and `null + non-zero` is rejected.
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

/// Representative destroy-function signature for any owned output buffers.
///
/// # Safety
///
/// The caller must pass either `ptr == null && len == 0` or a pointer/length
/// pair that originated from a future `units-x` owned-output allocation
/// contract.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn units_x_owned_buffer_destroy(
    buffer: units_x_owned_bytes,
) -> units_x_status {
    if !buffer.is_contract_valid() {
        if buffer.ptr.is_null() {
            return units_x_status::UNITS_X_STATUS_NULL_WITH_LENGTH;
        }
        return units_x_status::UNITS_X_STATUS_INVALID_OWNED_BUFFER;
    }
    if buffer.ptr.is_null() && buffer.len_bytes != 0 {
        return units_x_status::UNITS_X_STATUS_NULL_WITH_LENGTH;
    }
    units_x_status::UNITS_X_STATUS_OK
}

#[cfg(test)]
mod tests {
    use super::*;
    use core::any::TypeId;
    use core::mem::size_of;
    use core::ptr;

    #[test]
    fn slice_contract_uses_u64_and_null_zero_rule() {
        let empty = distance_mm_i32_slice {
            ptr: ptr::null(),
            len: 0,
        };
        let invalid = distance_mm_i32_slice {
            ptr: ptr::null(),
            len: 1,
        };
        let invalid_non_null_empty = distance_mm_i32_slice {
            ptr: &distance_mm_i32 { value_mm: 1 },
            len: 0,
        };

        assert!(empty.is_contract_valid());
        assert!(!invalid.is_contract_valid());
        assert!(!invalid_non_null_empty.is_contract_valid());
        assert_eq!(
            size_of::<distance_mm_i32_slice>(),
            size_of::<(*const distance_mm_i32, u64)>()
        );
    }

    #[test]
    fn unit_marker_names_remain_distinct() {
        assert_ne!(TypeId::of::<mm>(), TypeId::of::<Mm>());
        assert_ne!(TypeId::of::<degC>(), TypeId::of::<degF>());
    }

    #[test]
    fn scalar_abi_wrapper_matches_payload_size() {
        assert_eq!(size_of::<distance_mm_i32>(), size_of::<i32>());
    }

    #[test]
    fn owned_buffer_contract_is_byte_explicit() {
        let empty = units_x_owned_bytes {
            ptr: ptr::null_mut(),
            len_bytes: 0,
            capacity_bytes: 0,
        };
        let invalid_null = units_x_owned_bytes {
            ptr: ptr::null_mut(),
            len_bytes: 1,
            capacity_bytes: 1,
        };
        let invalid_capacity = units_x_owned_bytes {
            ptr: core::ptr::dangling_mut::<c_void>(),
            len_bytes: 8,
            capacity_bytes: 4,
        };

        assert!(empty.is_contract_valid());
        assert!(!invalid_null.is_contract_valid());
        assert!(!invalid_capacity.is_contract_valid());
        assert_eq!(
            size_of::<units_x_owned_bytes>(),
            size_of::<(*mut c_void, u64, u64)>()
        );
    }

    #[test]
    fn status_abi_surface_is_fixed_width() {
        assert_eq!(size_of::<units_x_status>(), size_of::<u32>());
    }
}
