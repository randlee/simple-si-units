#![allow(non_camel_case_types)]

pub use crate::generated::ffi_contract_types::{
    distance_mm_i32, distance_mm_i32_slice, distance_mm_i32_slice_mut,
};
pub use crate::generated::public_types::{degC, degF, m, mm};
pub type quantity<Unit, Storage> = crate::model::Quantity<Unit, Storage>;
use core::ffi::{c_char, c_void};
use core::slice;
use std::vec::Vec;

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
    UNITS_X_STATUS_ARITHMETIC_OVERFLOW = 2,
    UNITS_X_STATUS_OWNED_OUTPUT_REQUIRED = 3,
    UNITS_X_STATUS_INVALID_OWNED_BUFFER = 4,
    UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW = 5,
    UNITS_X_STATUS_OWNED_BUFFER_RANGE_OVERFLOW = 6,
}

fn status_from_u32(status: u32) -> Option<units_x_status> {
    match status {
        0 => Some(units_x_status::UNITS_X_STATUS_OK),
        1 => Some(units_x_status::UNITS_X_STATUS_NULL_WITH_LENGTH),
        2 => Some(units_x_status::UNITS_X_STATUS_ARITHMETIC_OVERFLOW),
        3 => Some(units_x_status::UNITS_X_STATUS_OWNED_OUTPUT_REQUIRED),
        4 => Some(units_x_status::UNITS_X_STATUS_INVALID_OWNED_BUFFER),
        5 => Some(units_x_status::UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW),
        6 => Some(units_x_status::UNITS_X_STATUS_OWNED_BUFFER_RANGE_OVERFLOW),
        _ => None,
    }
}

fn status_code_ptr(status: u32) -> *const c_char {
    match status_from_u32(status) {
        Some(units_x_status::UNITS_X_STATUS_OK) => c"ok".as_ptr(),
        Some(units_x_status::UNITS_X_STATUS_NULL_WITH_LENGTH) => c"null_with_length".as_ptr(),
        Some(units_x_status::UNITS_X_STATUS_ARITHMETIC_OVERFLOW) => c"arithmetic_overflow".as_ptr(),
        Some(units_x_status::UNITS_X_STATUS_OWNED_OUTPUT_REQUIRED) => {
            c"owned_output_required".as_ptr()
        }
        Some(units_x_status::UNITS_X_STATUS_INVALID_OWNED_BUFFER) => {
            c"invalid_owned_buffer".as_ptr()
        }
        Some(units_x_status::UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW) => {
            c"slice_length_overflow".as_ptr()
        }
        Some(units_x_status::UNITS_X_STATUS_OWNED_BUFFER_RANGE_OVERFLOW) => {
            c"owned_buffer_range_overflow".as_ptr()
        }
        None => c"unknown_status".as_ptr(),
    }
}

fn status_description_ptr(status: u32) -> *const c_char {
    match status_from_u32(status) {
        Some(units_x_status::UNITS_X_STATUS_OK) => c"operation completed successfully".as_ptr(),
        Some(units_x_status::UNITS_X_STATUS_NULL_WITH_LENGTH) => {
            c"null pointers must only be paired with zero lengths".as_ptr()
        }
        Some(units_x_status::UNITS_X_STATUS_ARITHMETIC_OVERFLOW) => {
            c"the computed quantity does not fit the requested storage type".as_ptr()
        }
        Some(units_x_status::UNITS_X_STATUS_OWNED_OUTPUT_REQUIRED) => {
            c"the caller must supply a writable output slot".as_ptr()
        }
        Some(units_x_status::UNITS_X_STATUS_INVALID_OWNED_BUFFER) => {
            c"owned buffers must use a pointer with capacity greater than or equal to length"
                .as_ptr()
        }
        Some(units_x_status::UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW) => {
            c"the incoming slice length does not fit the host usize ABI".as_ptr()
        }
        Some(units_x_status::UNITS_X_STATUS_OWNED_BUFFER_RANGE_OVERFLOW) => {
            c"the owned buffer byte range does not fit the host usize ABI".as_ptr()
        }
        None => {
            c"the supplied status code is outside the published units-x status contract".as_ptr()
        }
    }
}

fn abi_len_to_usize_with_status(
    len: u64,
    max_value: u64,
    overflow_status: units_x_status,
) -> Result<usize, units_x_status> {
    if len > max_value {
        return Err(overflow_status);
    }
    Ok(len as usize)
}

fn abi_slice_len_to_usize(len: u64) -> Result<usize, units_x_status> {
    abi_len_to_usize_with_status(
        len,
        usize::MAX as u64,
        units_x_status::UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW,
    )
}

fn abi_owned_range_to_usize(len: u64) -> Result<usize, units_x_status> {
    abi_len_to_usize_with_status(
        len,
        usize::MAX as u64,
        units_x_status::UNITS_X_STATUS_OWNED_BUFFER_RANGE_OVERFLOW,
    )
}

/// Stable machine-readable status code for foreign-language recovery logic.
#[unsafe(no_mangle)]
pub extern "C" fn units_x_status_code(status: u32) -> *const c_char {
    status_code_ptr(status)
}

/// Stable human-readable status description for logs and diagnostics.
#[unsafe(no_mangle)]
pub extern "C" fn units_x_status_description(status: u32) -> *const c_char {
    status_description_ptr(status)
}

/// Representative scalar-returning ABI export shape.
///
/// # Safety
///
/// `input` must follow the null-plus-zero slice contract documented by
/// `distance_mm_i32_slice`. `out` must be either null or a valid writable
/// pointer to a `distance_mm_i32` output slot owned by the caller.
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
    if input.len == 0 {
        unsafe { out.write(distance_mm_i32 { value_mm: 0 }) };
        return units_x_status::UNITS_X_STATUS_OK;
    }
    let Ok(len) = abi_slice_len_to_usize(input.len) else {
        return units_x_status::UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW;
    };
    let values = unsafe { slice::from_raw_parts(input.ptr, len) };
    let total = values
        .iter()
        .fold(0_i64, |acc, item| acc + i64::from(item.value_mm));
    let Ok(value_mm) = i32::try_from(total) else {
        return units_x_status::UNITS_X_STATUS_ARITHMETIC_OVERFLOW;
    };
    unsafe { out.write(distance_mm_i32 { value_mm }) };
    units_x_status::UNITS_X_STATUS_OK
}

/// Representative destroy-function signature for any owned output buffers.
///
/// # Safety
///
/// `buffer` must either be the null-plus-zero sentinel or an owned buffer
/// returned by the `units-x` ABI with matching pointer, length, and capacity
/// fields expressed in bytes.
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
    if buffer.ptr.is_null() {
        return units_x_status::UNITS_X_STATUS_OK;
    }
    let Ok(len_bytes) = abi_owned_range_to_usize(buffer.len_bytes) else {
        return units_x_status::UNITS_X_STATUS_OWNED_BUFFER_RANGE_OVERFLOW;
    };
    let Ok(capacity_bytes) = abi_owned_range_to_usize(buffer.capacity_bytes) else {
        return units_x_status::UNITS_X_STATUS_OWNED_BUFFER_RANGE_OVERFLOW;
    };
    unsafe {
        drop(Vec::from_raw_parts(
            buffer.ptr.cast::<u8>(),
            len_bytes,
            capacity_bytes,
        ))
    };
    units_x_status::UNITS_X_STATUS_OK
}

#[cfg(test)]
mod tests {
    use super::*;
    use core::any::TypeId;
    use core::mem::size_of;
    use core::ptr;
    use std::ffi::CStr;

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
        assert_ne!(TypeId::of::<mm>(), TypeId::of::<m>());
        assert_ne!(TypeId::of::<degC>(), TypeId::of::<degF>());
    }

    #[test]
    fn scalar_abi_wrapper_matches_payload_size() {
        assert_eq!(size_of::<distance_mm_i32>(), size_of::<i32>());
    }

    #[test]
    fn slice_sum_writes_result_before_reporting_success() {
        let values = [
            distance_mm_i32 { value_mm: 2 },
            distance_mm_i32 { value_mm: 3 },
            distance_mm_i32 { value_mm: 5 },
        ];
        let input = distance_mm_i32_slice {
            ptr: values.as_ptr(),
            len: values.len() as u64,
        };
        let mut out = distance_mm_i32 { value_mm: 0 };

        let status = unsafe { units_x_distance_mm_i32_slice_sum(input, &mut out) };

        assert_eq!(status, units_x_status::UNITS_X_STATUS_OK);
        assert_eq!(out.value_mm, 10);
    }

    #[test]
    fn slice_sum_reports_arithmetic_overflow_for_i32_overflow() {
        let values = [
            distance_mm_i32 { value_mm: i32::MAX },
            distance_mm_i32 { value_mm: 1 },
        ];
        let input = distance_mm_i32_slice {
            ptr: values.as_ptr(),
            len: values.len() as u64,
        };
        let mut out = distance_mm_i32 { value_mm: 0 };

        let status = unsafe { units_x_distance_mm_i32_slice_sum(input, &mut out) };

        assert_eq!(status, units_x_status::UNITS_X_STATUS_ARITHMETIC_OVERFLOW);
        assert_eq!(out.value_mm, 0);
    }

    #[test]
    fn slice_sum_accepts_documented_empty_sentinel() {
        let input = distance_mm_i32_slice {
            ptr: ptr::null(),
            len: 0,
        };
        let mut out = distance_mm_i32 { value_mm: -1 };

        let status = unsafe { units_x_distance_mm_i32_slice_sum(input, &mut out) };

        assert_eq!(status, units_x_status::UNITS_X_STATUS_OK);
        assert_eq!(out.value_mm, 0);
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

    #[test]
    fn owned_buffer_destroy_accepts_owned_vec_contract() {
        let mut bytes = vec![1_u8, 2, 3, 4];
        let buffer = units_x_owned_bytes {
            ptr: bytes.as_mut_ptr().cast::<c_void>(),
            len_bytes: bytes.len() as u64,
            capacity_bytes: bytes.capacity() as u64,
        };
        core::mem::forget(bytes);

        let status = unsafe { units_x_owned_buffer_destroy(buffer) };

        assert_eq!(status, units_x_status::UNITS_X_STATUS_OK);
    }

    #[test]
    fn abi_slice_len_conversion_reports_overflow_status() {
        let status = abi_len_to_usize_with_status(
            5,
            4,
            units_x_status::UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW,
        )
        .unwrap_err();

        assert_eq!(status, units_x_status::UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW);
    }

    #[test]
    fn abi_owned_buffer_conversion_reports_overflow_status() {
        let status = abi_len_to_usize_with_status(
            9,
            8,
            units_x_status::UNITS_X_STATUS_OWNED_BUFFER_RANGE_OVERFLOW,
        )
        .unwrap_err();

        assert_eq!(
            status,
            units_x_status::UNITS_X_STATUS_OWNED_BUFFER_RANGE_OVERFLOW
        );
    }

    #[test]
    fn status_code_and_description_exports_are_stable() {
        let code = unsafe {
            CStr::from_ptr(units_x_status_code(
                units_x_status::UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW as u32,
            ))
        }
        .to_str()
        .unwrap();
        let description = unsafe {
            CStr::from_ptr(units_x_status_description(
                units_x_status::UNITS_X_STATUS_SLICE_LENGTH_OVERFLOW as u32,
            ))
        }
        .to_str()
        .unwrap();
        let unknown = unsafe { CStr::from_ptr(units_x_status_code(99)) }
            .to_str()
            .unwrap();

        assert_eq!(code, "slice_length_overflow");
        assert_eq!(
            description,
            "the incoming slice length does not fit the host usize ABI"
        );
        assert_eq!(unknown, "unknown_status");
    }
}
