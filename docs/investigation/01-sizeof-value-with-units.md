# Size And Layout Investigation

## Conclusion

For the current implementation, a value-with-units is the same size and alignment as its underlying numeric payload.

Reason:

- Each unit type is a single-field generic struct, for example [Amount<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:26) and [Distance<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2039).
- The proc macro adds trait impls, not extra fields, as seen in [simple-si-units-macros/src/lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units-macros/src/lib.rs:64).

## Measured values

Measured by compiling a small probe program against the local crate build:

| Type | Size (bytes) | Alignment |
|---|---:|---:|
| `Distance<f64>` | 8 | 8 |
| `Distance<f32>` | 4 | 4 |
| `Time<f64>` | 8 | 8 |
| `Mass<f64>` | 8 | 8 |
| `Area<f64>` | 8 | 8 |
| `Velocity<f64>` | 8 | 8 |
| `Distance<i128>` | 16 | 16 |

## Important caveat

This is a practical Rust-layout property, not a formal FFI guarantee.

Why:

- The structs do not declare `#[repr(C)]` or `#[repr(transparent)]`.
- Rust is therefore free to treat layout as an internal language detail, even though a one-field struct currently behaves as expected.

## What this means in practice

Inside Rust:

- Treat these types as effectively zero-overhead wrappers around the numeric value.

Across FFI boundaries:

- Do not assume the observed layout is stable enough for C, Python extension modules, or .NET interop without adding an explicit representation guarantee in a wrapper layer.
