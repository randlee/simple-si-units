# Product Requirements Document

## Project

Unit-preserving, minimum-footprint quantities crate with stable C ABI and clean serialization paths.

## Summary

This project will create a new crate as the deliverable. The existing `simple-si-units`, `simple-si-units-core`, and `simple-si-units-macros` crates will remain in the repository under `reference/` as reference implementations, conversion-factor sources, and validation oracles, but will not be the primary shipped design for this effort.

The new crate will provide:

- unit-preserving quantity types
- minimum storage footprint
- cross-platform stable binary layout at the ABI boundary
- clean JSON and binary serialization paths
- support for non-SI units
- support for scalar values and arrays/buffers
- explicit conversion into canonical compute-friendly forms for derivative calculations
- code generation driven by a master unit catalog

## Problem Statement

The current crate design is compute-first:

- values are normalized into canonical SI storage
- for example, `Distance<T>` always stores meters
- the types are Rust-native and generic
- the public layout is not a stable C ABI

That is useful for Rust computations, but it does not satisfy the desired requirements:

- preserve the original declared unit such as `mm` or `cm`
- use the absolute smallest storage possible
- support compact arrays and buffers
- provide stable interop with Python and C-family consumers
- allow both JSON and binary serialization without ambiguity
- allow new units to be added over time without broad manual code edits

## Product Goals

### Primary goals

1. Create a new crate that is the real deliverable.
2. Preserve units at the type level and storage boundary.
3. Make storage footprint equal to the footprint of the underlying storage type or buffer.
4. Provide a stable C ABI for foreign-language interop.
5. Provide first-class JSON and binary serialization paths.
6. Support non-SI units in a principled way.
7. Make the master unit catalog the source of truth for generated code, wrappers, and tests.

### Secondary goals

1. Reuse unit metadata and conversion relationships from the current project unless a documented incompatibility requires replacement.
2. Allow easy bridging to canonical compute types for derivative math.
3. Keep the design appropriate for PyO3/maturin and Interoptopus.
4. Make it easy for maintainers and end users to extend the unit set by editing catalog data and regenerating artifacts.

## Non-Goals

1. Reworking the current `simple-si-units` crate in place.
2. Preserving arbitrary operand-order-dependent derived-unit output types for all multiplication and division combinations.
3. Solving every possible dimensional-analysis problem in the first release.
4. Supporting every offset unit in v1.

## Deliverable Strategy

### Existing crates

The current crates remain:

- reference implementation
- source of unit definitions
- source of conversion factors
- source of operator relationship knowledge
- regression oracle for validation
- housed under `reference/`

### New crate

The new crate will become the product deliverable.

It will own:

- stable storage representation
- unit-preserving quantity model
- array and buffer wrappers
- foreign-function boundary types
- JSON and binary serialization strategy
- explicit conversion to canonical compute types
- catalog-driven generation pipeline

## Repository Layout

The repository layout must be explicit:

- `reference/` contains the legacy `simple-si-units*` crates kept for investigation, parity checks, and source extraction
- `crates/` contains the new Rust workspace members that are intended to ship
- `python/` contains the Python package, PyO3 bindings, generated Pydantic models, and packaging assets
- `dotnet/` contains the generated or partly generated C# wrapper/package and shared `.NET` build metadata such as `Directory.Build.props`

The planned shipped Rust crates are not to live at the repository root.

## Publication Targets

The project must support these publication targets:

- Rust crates published from `crates/` to `crates.io`
- the Python package published from `python/` for normal `pip install` consumption and PyPI publication
- the `.NET` package published from `dotnet/` to `nuget.org`

## Version Source Of Truth

All shipped artifacts must share one version source of truth.

Requirements:

1. One machine-readable version file must be the only manually edited version source.
2. Rust `Cargo.toml` package versions must be synchronized from that source.
3. `.NET` package versions, including `Directory.Build.props`, must be synchronized from that source.
4. Python package metadata, including the `maturin`/`pyproject.toml` version path, must be synchronized from that source.
5. A verification test must fail in normal local test entrypoints and in CI if any published artifact version drifts from the shared source.
6. `just test` and the default CI validation path must both include this version-lock check.

## Source Of Truth Requirement

The project must define a master unit catalog as the authoritative source of truth for:

- dimensions
- human-readable unit symbols
- code-facing unit ids
- binary-safe unit ids
- display names
- canonical base units
- scale factors
- offsets where applicable
- aliases
- JSON names
- JSON type ids
- JSON encoding form for each public type
- binary schema ids
- ABI type naming inputs
- wrapper-generation inputs
- test-generation inputs

The project should not require hand-maintained duplication of this data across Rust, Python, C#, Go, and test code.

Adding a new unit should ideally be accomplished by editing the master catalog and rerunning generation.

The version source-of-truth file is separate from the unit catalog, but it must follow the same principle: one editable source, generated consumers, and failing verification on drift.

## Core Design

## 1. Unit-preserving quantities

The new design will use unit-preserving storage types instead of canonical-SI-internal wrappers.

Representative shape:

```rust
#[repr(transparent)]
pub struct Quantity<Unit, Storage> {
    pub storage: Storage,
    _unit: core::marker::PhantomData<Unit>,
}
```

Where:

- `Unit` is a zero-sized marker type
- `Storage` is the actual payload

Examples:

- `Quantity<mm, i32>`
- `Quantity<cm, f32>`
- `Quantity<m, [i16; 1024]>`
- `Quantity<ft, Vec<i32>>`

The unit marker is type-level only and must not add runtime storage overhead.

## 2. Minimum footprint

The storage size of a quantity must be the same as the size of its `Storage`.

Examples:

- `Quantity<mm, i32>` must be 4 bytes
- `Quantity<cm, f32>` must be 4 bytes
- `Quantity<cm, [i16; 256]>` must be the same size as `[i16; 256]`
- `Quantity<cm, Vec<i16>>` must be the same size as `Vec<i16>`

There must be no per-element wrapper overhead for arrays or vectors.

## 3. Stable C ABI

The project must support a clean stable ABI for C-family interop.

Requirements:

1. FFI-facing scalar wrapper types must use `#[repr(C)]` or `#[repr(transparent)]`.
2. FFI-facing array/buffer forms must use explicit pointer-plus-length structs.
3. Generic Rust-only types may exist internally, but the public foreign boundary must use concrete monomorphic types.
4. Endianness, numeric width, and field order must be explicitly documented for binary interchange.

Representative FFI forms:

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
```

These ABI slice structs are in-memory interop views only. They are not themselves the binary wire format.

## Unit Model

## 1. Supported unit categories

V1 will support unit markers for the full unit families currently considered in
scope from the reference project:

- `base`
- `geometry`
- `mechanical`
- `electromagnetic`

This includes both base quantities and derived quantities across those
families.

The authoritative MVP public type inventory is defined in
`catalog/generated/units-catalog-summary.json`.
[docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md)
is a derived checklist for human review and planning readability.

## 2. Support for non-SI units

The new crate will support non-SI units.

Examples for distance:

- `mm`
- `cm`
- `m`
- `km`
- `in`
- `ft`
- `yd`
- `mi`

Examples for velocity:

- `mps`
- `kph`
- `mph`

Examples for mass:

- `g`
- `kg`
- `lb`

Examples for temperature:

- code id `K`, wire/display unit `K`
- code id `degC`, wire/display unit `C`
- code id `degF`, wire/display unit `F`

V1 should prioritize multiplicative units with scale-only conversion, but the MVP/V1 scope must also include Celsius and Fahrenheit as the initial offset-unit set.

Other offset units remain deferred unless deliberately added later.

## 2a. Reciprocal and domain-specific public units

Reciprocal quantities are required when they correspond to real public domain
units rather than only algebra artifacts.

Example:

- inverse distance must support `Diopter` as a first-class public quantity
- `1 dpt = 1 / m`

The public API should therefore expose the domain unit name when one exists,
while the catalog and dimensional model preserve the underlying reciprocal
relationship.

## 3. Unit marker naming

Unit marker type names should use the same case as the displayed unit symbol wherever Rust identifiers allow it.

Implications:

- case is semantically significant and must not be normalized away
- distinct units may differ only by case, such as `mm` versus `Mm`
- preserving symbol case takes precedence over Rust CamelCase conventions for marker types when those goals conflict
- symbols that are not valid or desirable as Rust identifiers must use a documented fallback spelling that preserves the meaningful case distinction, such as `degC` and `degF` for the human-readable wire/display symbols `C` and `F`
- wire/display symbols remain human-readable even when code identifiers use a fallback spelling; for example, code may use `degC` while JSON and display use `C`

## 4. Conversion model

Each unit marker will define conversion to a canonical base unit for its dimension.

Representative trait shape:

```rust
pub trait DistanceUnit {
    const METERS_PER_UNIT: f64;
    const SYMBOL: &'static str;
}
```

Scale-only constants are sufficient for multiplicative units. Offset units in
V1, specifically Celsius and Fahrenheit, require explicit additive-offset
conversion logic relative to the canonical temperature unit.

These conversion rules should be derived from the master catalog, not duplicated manually across language surfaces.

This allows:

- unit-preserving storage
- explicit canonical conversion for computation
- clean JSON metadata
- clean binary schema documentation
- catalog-driven generation of language bindings and tests

## Arithmetic Semantics

## 1. Scalar operations

Scalar operations must preserve the declared unit.

Examples:

- `Quantity<cm, i32> * i32 -> Quantity<cm, i32>`
- `Quantity<ft, f32> * f32 -> Quantity<ft, f64>`

## 2. Addition and subtraction

Addition and subtraction between compatible units must be supported.

The result should preserve the left-hand unit by converting the right-hand side into the left-hand unit.

Example:

- `distance_mm + distance_m -> distance_mm`

This behavior should be explicit and documented.

When storage types differ, arithmetic must use a deterministic promotion rule rather than implicitly preserving the left-hand storage width. In V1, unit preservation and storage promotion are separate rules.

## 3. Derived calculations

Derived calculations must be supported, but they should favor canonical compute outputs rather than operand-order-dependent exotic unit outputs.

Examples:

- `Distance / Time -> Velocity`
- `Velocity / Time -> Acceleration`
- `Velocity * Time -> Distance`:
  deferred beyond Sprint B-3; V1 closes first on the free-function compute
  bridges `velocity_from_distance_and_time` and
  `acceleration_from_velocity_and_time`

Recommended behavior:

- base quantity storage preserves units
- derived calculations normalize into canonical derived compute units unless explicitly requested otherwise

This avoids combinatorial API explosion and order-dependent result-type surprises.

Full legacy operator-graph parity for every possible unit combination is not
required for V1, as long as:

- all in-scope unit families are cataloged and exposed
- conversion and serialization work for those units
- explicitly documented derived calculations are supported
- domain-important reciprocal units such as `Diopter` are first-class public types

## Arrays And Buffers

The crate must support arrays and buffers as first-class payloads.

Examples:

- `Quantity<cm, [i16; N]>`
- `Quantity<cm, Vec<i32>>`
- `Quantity<cm, Box<[f32]>>`
- borrowed slice views for the planned Rust-only bulk APIs

Goals:

- one wrapper around the entire collection
- no per-element object overhead
- simple binary serialization
- easy foreign-language mapping

## Serialization Requirements

## 1. JSON path

The crate must provide a clean JSON serialization model.

JSON must be:

- unambiguous
- self-describing enough for external consumers
- stable across platforms
- canonical across language bindings

Recommended scalar shape:

```json
{
  "type": "distance_i32",
  "unit": "mm",
  "value": 1250
}
```

Recommended fixed small-buffer shape:

```json
{
  "type": "distance3_i16",
  "unit": "cm",
  "values": [12, 15, 18]
}
```

Recommended large/arbitrary-buffer shape:

```json
{
  "type": "distance_buffer_i16",
  "unit": "cm",
  "encoding": "base64-le",
  "count": 16384,
  "values_b64": "..."
}
```

Requirements:

1. JSON serialization must not rely on implicit field naming from internal Rust storage.
2. Unit symbols must be explicit in JSON and should be human-readable, such as `C` rather than `degC`.
3. The machine-readable `type` field is the canonical schema/type discriminator.
4. The same canonical wire shape must be used by Rust, Python, and C#.
5. The JSON schema must be suitable for generated Pydantic models and generated or adjacent `System.Text.Json` DTOs without per-language shape drift.
6. Canonical serializer output is defined per type and must not switch format dynamically based on runtime buffer length alone.
7. Deserializers may accept more than one supported input form where explicitly documented, but serializers emit exactly one canonical form per type.

Canonical JSON policy:

- scalar types use the compact `type` + `unit` + `value` shape
- small fixed-size buffer types may use JSON arrays for readability
- arbitrary-length or large buffer types use explicit encoded payload envelopes
- the chosen JSON form is a machine-readable catalog property of the public type, not a serializer guess based on runtime length
- canonical parity is semantic equality against shared fixtures, not byte-for-byte serializer identity or key-order identity
- non-finite floating-point values are out of scope for the canonical JSON format unless a later explicit policy is added

Implementation direction:

- `serde` support
- explicit custom serialized representation where needed
- schema-first generation for language models and wrappers
- catalog-driven schema and fixture generation

## 2. Binary path

The crate must provide a clean binary serialization model.

Binary format goals:

- minimal footprint
- zero ambiguity
- deterministic cross-platform interpretation

Requirements:

1. The unit is schema-level or header-level metadata, not duplicated per element.
2. Endianness must be defined.
3. Numeric width must be defined.
4. Array payloads should be raw contiguous numeric storage where possible.
5. The binary wire format must be documented separately from the in-memory ABI layout.
6. The binary envelope must include a wire-format versioning policy and schema identification policy.

Recommended approach:

- raw payload bytes for the numeric storage
- explicit metadata envelope at protocol boundaries when needed
- optional helper APIs for packing and unpacking

Example binary schema concept:

- header: wire-format version, schema id, binary-safe unit id, storage type id, length
- payload: tightly packed little-endian numeric array

For extremely constrained environments, raw payload plus out-of-band schema is also acceptable.

## Cross-Language Interop Requirements

## 1. Python via PyO3/maturin

The design must support an ergonomic Python wrapper crate.

Requirements:

1. Rust core remains the authoritative implementation.
2. Python-facing classes expose explicit unit-specific types or constructors.
3. Buffer-friendly APIs should be possible for lists, arrays, or NumPy-compatible paths later.
4. Python high-level bulk APIs may use the same wire-format semantics while remaining separate from raw pointer-plus-length ABI structs.

Representative usage direction:

- `DistanceMmI32`
- `DistanceCmArrayI16`
- explicit conversion methods
- explicit compute bridge methods

## 2. C# via Interoptopus

The design must support a stable exported C ABI suitable for Interoptopus and .NET.

Requirements:

1. Exported types must be concrete and ABI-stable.
2. Exported functions must be explicit and avoid trait/operator assumptions.
3. Slices and arrays must use explicit pointer-plus-length forms with fixed-width lengths.

Representative exported functions:

- `distance_mm_i32_to_m_f64`
- `distance_cm_i16_add_distance_m_f64_as_cm_f64`
- `velocity_mps_f64_from_distance_m_f64_and_time_s_f64`

## Relationship To Existing Project

The current codebase should be reused where it helps, but not forced into the new design.

What should be reused:

- unit catalogs
- conversion-factor source data
- operator relationship source data
- validation comparisons

What should not be reused directly:

- canonical-SI internal storage model
- current generic public API as the stable foreign boundary

## Code Generation Requirements

Code generation is a first-class part of the design.

It must be used to generate or assist generation of:

1. unit marker definitions
2. conversion tables
3. ABI type names and exported function inventories
4. JSON schemas and fixtures
5. Pydantic models or their inputs
6. C# JSON DTOs or their inputs
7. C# convenience bindings
8. reference-based tests driven from catalog data

The generation pipeline must be structured so that end users can extend the unit set with minimal manual work, ideally by editing the master catalog and rerunning generation.

The catalog must carry enough metadata to support:

- human-readable unit symbols distinct from code identifiers where necessary
- binary-safe unit ids distinct from display symbols
- machine-readable JSON encoding-form selection for each public type
- language-specific reserved-word and naming-collision handling
- offset-conversion rules
- stable schema id evolution
- generated function inventories for supported conversions and compute bridges

## Validation Requirements

The new crate must be validated against the existing project where applicable.

Examples:

1. Conversion equivalence checks against the existing reference crate
2. Derived calculation equivalence for canonical compute outputs
3. Size/layout assertions for ABI-facing types
4. Serialization round-trip tests for JSON
5. Binary conformance tests for documented wire layout
6. Cross-language JSON shape parity tests
7. Catalog-driven conversion tests for all declared units

## Release Scope

## V1 scope

V1 must include:

1. New crate with unit-preserving quantity design
2. Public type coverage matching
   [docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md)
3. Catalog-declared SI and non-SI multiplicative units, plus Celsius and Fahrenheit in the initial offset-temperature set
4. Scalar and array/buffer storage forms
5. JSON serialization path
6. Binary serialization path
7. Stable C ABI boundary types
8. Bridge into canonical compute operations
9. Canonical JSON wire-shape generation artifacts for Python and C#
10. Master catalog plus generation pipeline for code, wrappers, and tests
11. `Diopter` as a first-class public reciprocal domain unit

## Deferred from V1

1. Offset units beyond Celsius and Fahrenheit
2. Arbitrary dimension algebra for every possible unit combination
3. Rich NumPy integration
4. `chemical` and `nuclear` unit families
5. Full legacy operator-graph parity for every possible unit combination

## Success Criteria

The project is successful when:

1. A distance stored as `mm`, `cm`, or `ft` can remain in that unit-preserving form for storage and interchange.
2. Scalar and array forms introduce no runtime storage overhead beyond the underlying numeric storage.
3. JSON and binary serialization are explicit, documented, and test-covered.
4. ABI-facing types are stable and suitable for foreign-language interop.
5. Python and C# wrappers can be built cleanly on top of the crate.
6. Canonical derivative calculations are available without sacrificing the storage model.
7. Python Pydantic models and C# `System.Text.Json` types can serialize the same on-the-wire JSON shape for every public type.
8. Adding a new unit is primarily a catalog-edit and regeneration workflow rather than a broad manual code-edit workflow.

## Next Step

After this PRD is accepted, the next phase will be foundation work covering:

1. repository and deliverable scaffolding
2. catalog and generation bootstrap
3. ABI and naming contract lock-in
4. CI and `sc-lint` baseline setup
