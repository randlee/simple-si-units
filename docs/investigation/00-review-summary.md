# Project Review Summary

## Scope

This review focused on:

1. `sizeof(value-with-units)` in bytes
2. Available serialization mechanisms
3. Readiness for exposure to other languages such as Python and .NET

I also ran the crate test matrix to identify review findings that materially affect maintainability and downstream adoption.

## Highest-priority findings

### 1. Default `cargo test` is broken

The default test configuration fails to compile because feature-specific unit tests are not gated behind the corresponding crate features. The failures start in the unconditional `BigFloat` and `Complex` tests at [simple-si-units/src/lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/lib.rs:2289) and [simple-si-units/src/lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/lib.rs:4085).

Observed behavior:

- `cargo test --quiet` fails
- `cargo test --all-features --quiet` passes

Impact:

- Contributors get a failing baseline unless they know to enable all optional features.
- CI or downstream packagers using the default feature set can get misleading failures.

## 2. `num-rational` support is documented but not actually wired up

The crate references `#[cfg(feature="num-rational")]` in [simple-si-units/src/lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/lib.rs:55), but `num-rational` is not declared as an optional dependency or feature in [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:17). The README comparison table still claims partial support in [simple-si-units/README.md](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/README.md:162).

Impact:

- `rustc` emits an `unexpected cfg` warning.
- Users evaluating numeric-type support get inaccurate guidance.

## Direct answers

### 1. What is `sizeof(value-with-units)`?

Empirically, for the tested current implementation, unit values are the same size and alignment as their underlying numeric type because each unit struct contains exactly one public field, for example [Distance<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2039).

Measured values on this machine:

- `Distance<f64>`: 8 bytes, align 8
- `Distance<f32>`: 4 bytes, align 4
- `Time<f64>`: 8 bytes, align 8
- `Mass<f64>`: 8 bytes, align 8
- `Area<f64>`: 8 bytes, align 8
- `Velocity<f64>`: 8 bytes, align 8
- `Distance<i128>`: 16 bytes, align 16

Important caveat:

- This is the current Rust layout in practice, not a stable ABI guarantee, because the structs do not use `#[repr(C)]` or `#[repr(transparent)]`.

### 2. What serialization methods are available?

The only built-in structured serialization surface is `serde`, enabled by the optional dependency in [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:24). Each unit struct conditionally derives `Serialize` and `Deserialize`, for example [Amount<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:24) and [Distance<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2037).

What the crate provides:

- `serde::{Serialize, Deserialize}` derives when the `serde` feature is enabled
- `fmt::Display` string formatting for human-readable output, for example [Amount display impl](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:58)
- Manual extraction through the public field or `to_*` methods

What the crate does not provide:

- No built-in JSON, CBOR, bincode, postcard, YAML, or MessagePack APIs
- No custom wire-format module
- No versioned schema or backward-compatibility policy

### 3. Is the library set up to easily expose to other languages?

Not directly.

Main blockers:

- Public unit types are generic, for example [Distance<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2039)
- There is no stable representation attribute such as `repr(C)` or `repr(transparent)`
- The public API is trait-heavy and Rust-idiomatic, with proc-macro-generated operator impls in [simple-si-units-macros/src/lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units-macros/src/lib.rs:64)
- There is no `cdylib`, `extern "C"` API, PyO3 module, or Interoptopus inventory crate

Practical conclusion:

- The library is a good Rust core.
- It is not currently set up as a drop-in cross-language boundary.
- A thin wrapper crate with concrete `f64` newtypes and a dedicated FFI/PyO3 surface would be the right approach.

## Verification performed

- Read manifests and public type definitions
- Inspected proc-macro output patterns
- Ran `cargo test --quiet`
- Ran `cargo test --all-features --quiet`
- Measured representative sizes with a small compiled probe program
