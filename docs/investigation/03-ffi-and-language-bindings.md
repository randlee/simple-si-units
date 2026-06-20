# FFI And Language Binding Investigation

## Short answer

The library is a good Rust-native core, but it is not currently set up for easy direct exposure to Python, .NET, or other non-Rust consumers.

## Why it is not FFI-ready today

### 1. The core public types are generic

Representative example:

- [Distance<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2039)

That is excellent for Rust ergonomics, but generic types are a poor direct FFI surface. Binding generators typically want concrete, monomorphic types.

### 2. There is no stable representation guarantee

The unit structs are plain Rust structs with no `repr(C)` or `repr(transparent)` annotation, for example [Amount<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:26) and [Distance<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2039).

That blocks safe direct ABI assumptions.

### 3. The API is centered on Rust traits and operator overloading

The proc macro generates a large Rust-idiomatic trait surface in [simple-si-units-macros/src/lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units-macros/src/lib.rs:64), including:

- `Add`, `Sub`, `Mul`, `Div`
- `Copy`, `Eq`, `Ord`, `Hash` where available
- Reference-based operator ergonomics

This is convenient for Rust, but not something PyO3 or Interoptopus can directly project as a clean foreign-language API without an adaptation layer.

### 4. There is no FFI crate surface

I did not find:

- `crate-type = ["cdylib"]`
- `extern "C"` exported functions
- PyO3 `#[pymodule]` or `#[pyclass]`
- Interoptopus inventory / exported symbols

## Python via PyO3/maturin

### Current state

PyO3 is not wired in at all.

### Practical path

The right path is a wrapper crate, not exposing the generic core types directly.

Recommended shape:

1. Create concrete wrapper types such as `DistanceF64`, `TimeF64`, `VelocityF64`
2. Give those wrappers explicit `#[repr(transparent)]` or keep them entirely inside PyO3 classes
3. Expose constructors and getters in meters or other canonical units
4. Keep the generic Rust API internal

Example boundary design:

- Python constructor takes `meters: float`
- Internal Rust code stores `simple_si_units::base::Distance<f64>`
- Python-facing methods expose `to_m()`, `to_km()`, etc.

This is straightforward, but it is a separate packaging effort.

## .NET via Interoptopus

### Current state

Interoptopus is not wired in at all.

### Practical path

Interoptopus will want a stable, concrete ABI:

1. Use non-generic exported structs or plain primitive arguments
2. Use `#[repr(C)]` or `#[repr(transparent)]`
3. Export plain functions instead of relying on Rust operators
4. Keep ownership and allocation rules explicit

Good shape:

- `#[repr(C)] pub struct DistanceF64 { pub m: f64 }`
- `extern "C"` functions such as `velocity_from_distance_time(distance: DistanceF64, time: TimeF64) -> VelocityF64`

Bad shape for FFI:

- Generic `Distance<T>`
- Trait-bounded APIs
- Rust operator overloading as the boundary

## Hidden risks

### Field names are part of serde shape

If you expose serialized units across language boundaries, the current field names like `m`, `mol`, `mps`, and `kgpm3` become external protocol details.

### Feature-driven behavior expands the surface area

Optional integrations in [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:24) are useful inside Rust but complicate any attempt to define a minimal stable foreign-language API.

### The default contributor experience is already inconsistent

Default `cargo test` fails while `cargo test --all-features` passes. That should be fixed before building new wrapper crates under `crates/`, the Python package under `python/`, or the `.NET` package under `dotnet/`.

## Recommendation

Do not try to bind this crate directly.

Instead:

1. Keep `simple-si-units` as the Rust core
2. Keep the legacy crate under `reference/` and build new Rust-facing wrappers or bridges under `crates/` as needed
3. Add the Python package under `python/`
4. Add the C/.NET wrapper package under `dotnet/`
5. Use concrete `f64`-based wrappers at the boundary
6. Add explicit representation guarantees in the boundary layer
