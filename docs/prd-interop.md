# Interop PRD

## Purpose

This document defines the ABI-first interoperability requirements for C, C#, Go, and Rust consumers.

It focuses on stable layout, blittable data, and predictable foreign-language bindings.

## Supported ecosystems

This interop design targets:

- C
- C#
- Go
- Rust

These ecosystems can all consume a stable raw C ABI cleanly if the exported types are concrete and layout-stable.

## Summary

The interop surface must be:

- concrete
- stable
- blittable where applicable
- pointer-and-length based for arrays
- explicit rather than trait- or operator-driven

The raw C ABI is the source of truth for cross-language interop.

The generated or maintained `.NET` wrapper/package is a first-class deliverable and must be compatible with publication to `nuget.org`.

## Goals

### Primary goals

1. Define a stable C ABI for quantity scalars and arrays.
2. Ensure public structs are ABI-compatible across C#/Go/C/Rust.
3. Enable ergonomic generated or partly generated bindings for C# and Go.
4. Preserve minimum-footprint storage at the ABI boundary.
5. Ensure C# can expose the same canonical JSON wire shape used by Rust and Python, either through ABI-compatible structs where practical or through generated adjacent DTOs.

### Secondary goals

1. Keep the exported ABI small and explicit.
2. Allow higher-level language wrappers to be user-friendly without changing the underlying ABI.
3. Minimize manual wrapper maintenance by generating interop artifacts from the master catalog where practical.

## Non-Goals

1. Exporting Rust generics as the public ABI.
2. Exporting trait-based or operator-overloaded APIs directly.
3. Using `Vec<T>` or Rust ownership semantics directly across the boundary.

## ABI Principles

## 1. Concrete scalar types only

Every exported quantity type must be concrete and monomorphic.

Examples:

- `distance_mm_i32`
- `distance_m_f64`
- `time_s_f64`
- `velocity_mps_f64`
- `temperature_degC_f64`

Representative shape:

```rust
#[repr(C)]
#[derive(Copy, Clone)]
pub struct distance_mm_i32 {
    pub value_mm: i32,
}
```

## 2. Arrays use pointer plus length

Arrays and spans must not cross the ABI boundary as language-native span types.

Exported ABI array forms must use explicit pointer-plus-length structs.

Representative shapes:

```rust
#[repr(C)]
pub struct distance_m_f64_slice {
    pub ptr: *const distance_m_f64,
    pub len: u64,
}

#[repr(C)]
pub struct distance_m_f64_slice_mut {
    pub ptr: *mut distance_m_f64,
    pub len: u64,
}
```

Lengths should be fixed-width ABI integers such as `u64` rather than `usize` where stable cross-platform ABI predictability is required.

## 3. No hidden allocation contracts in V1

V1 should avoid APIs that require the foreign caller to understand Rust allocation internals.

Preferred patterns:

- caller-provided output buffer
- in-place mutation with explicit mutable slice types
- returned scalar values by value

Avoid in V1:

- returning Rust-owned heap allocations unless accompanied by explicit destroy functions and strict ownership rules

## Function Design Requirements

The exported ABI functions must be explicit and descriptive.

Examples:

- `distance_mm_i32_to_m_f64`
- `temperature_degC_f64_to_degF_f64`
- `velocity_mps_f64_from_distance_m_f64_and_time_s_f64`
- `distance_m_f64_scale_in_place`

Required characteristics:

1. explicit unit in function naming
2. explicit storage type in function naming where relevant
3. explicit input and output quantity types
4. explicit error signaling for slice/buffer operations

## Language-specific expectations

## 1. C

The C experience is the canonical raw ABI.

Requirements:

- generated or maintained C headers
- predictable struct layout
- no Rust-specific semantics exposed

## 2. C#

The public C# structs must be:

- blittable
- ABI-compatible with the raw C structs
- suitable for direct use in `Span<T>` and `ReadOnlySpan<T>` where layout permits

Recommended approach:

1. low-level generated bindings from the C ABI
2. generated or partial ergonomic wrappers on top
3. a package layout under `dotnet/` with centralized metadata in `Directory.Build.props`

Examples of desired C# usage:

- `DistanceMF64 value`
- `Span<DistanceMF64> values`
- `ReadOnlySpan<DistanceMF64> input`

The public C# quantity structs should be layout-compatible with the ABI structs so they can be pinned and passed efficiently.

The `.NET` package must also expose user-facing C# interfaces so application
code can depend on stable, ergonomic contracts rather than directly on raw
blittable structs alone.

Generated or adjacent DTO types are acceptable for `System.Text.Json` when that produces a cleaner or more maintainable surface, as long as the canonical wire shape does not drift.

## 3. Go

Go should consume the same C ABI through cgo or an equivalent layer.

Requirements:

- concrete C-compatible structs
- slice bridging via pointer plus length
- no dependency on Rust-specific features

Go-facing ergonomics may live in a small Go wrapper package on top of the raw cgo surface.

## 4. Rust

Rust itself may use richer internal generics and zero-sized marker types, but the exported interop boundary must remain concrete and ABI-stable.

The project may therefore have:

1. internal Rust-native types
2. explicit exported ABI types
3. conversion glue between them

## C# wrapper strategy

Interoptopus should generate the low-level P/Invoke layer from the raw ABI.

On top of that, the project should provide or support generation of user-friendly C# helpers.

Recommended layers:

1. generated low-level ABI bindings
2. generated partial structs for convenience members
3. generated span helpers for slice conversions
4. minimal handwritten extension layer only if needed
5. catalog-driven regeneration path for newly added units

Examples of ergonomic C# features:

- `Value` property
- C# interfaces for scalar and bulk quantity contracts
- unit-aware `ToString()`
- static constructors
- span-based batch APIs
- generated or adjacent `System.Text.Json` compatibility for the canonical wire shape
- NuGet-ready packaging metadata

## Span requirements for C#

`Span<T>` and `ReadOnlySpan<T>` are a C# API concern, not an ABI concern.

Requirements:

1. the underlying ABI structs must be blittable and sequentially laid out
2. the C# public quantity structs should remain compatible with pinning and span usage
3. the ABI must still use pointer plus length underneath

This allows clean projections like:

- `Span<DistanceMF64>`
- `ReadOnlySpan<TemperatureDegCF64>`

without exposing span types in the ABI itself.

## Serialization and ABI relationship

The interop ABI and the binary serialization format must be deliberately related but explicitly separate contracts.

Goals:

- predictable layout
- minimal copy behavior
- explicit unit and storage schema
- one canonical JSON wire shape across languages

Clarification:

- in-memory ABI structs define how languages call functions and share process memory
- binary wire formats define on-wire and on-disk payloads
- pointer-plus-length ABI structs are never themselves the serialized wire image
- the two contracts should share schema ids and semantics, but they must not be conflated

## JSON Interop Requirements

For JSON-facing interop, C# must be able to serialize and deserialize the canonical wire shape through ABI-compatible types where practical or through generated adjacent DTOs where that is cleaner.

Requirements:

1. The C# JSON surface must align exactly with the Rust canonical schema.
2. `System.Text.Json` serialization must match the Python Pydantic output and Rust reference fixtures semantically against canonical fixtures.
3. If separate ABI structs and JSON DTO structs are needed in C#, the mapping between them must be generated or trivial and must not change the wire shape.
4. Canonical JSON parity does not require byte-for-byte serializer identity or key-order identity.
5. Non-finite floating-point values are out of scope for canonical JSON unless a later explicit policy is added.
6. For selected large or opaque types, a Rust-backed converter path is acceptable if it preserves the same canonical wire shape and remains operationally maintainable.

Binary payloads for arrays should be representable as:

- metadata envelope plus raw contiguous numeric payload
- or raw payload plus out-of-band schema where appropriate

The preferred in-memory ABI bulk representation is a slice of ABI-facing scalar quantity wrappers, while the preferred binary wire representation is metadata plus raw numeric payload bytes.

C# JSON DTOs target the canonical wire representation rather than the in-memory ABI wrapper layout.

## Validation Requirements

The interop layer must include:

1. size and alignment assertions for ABI structs
2. C ABI smoke tests
3. C# binding validation
4. Go binding validation
5. round-trip tests for scalar and slice operations
6. binary layout conformance tests
7. `System.Text.Json` parity tests against canonical JSON fixtures
8. catalog-driven wrapper generation validation
9. shared-version synchronization validation against `Directory.Build.props`

## V1 Scope

V1 must include:

1. stable scalar quantity ABI structs
2. stable slice and mutable-slice ABI structs
3. explicit conversion functions
4. explicit canonical compute functions
5. C#-friendly generated surface
6. Go-consumable raw ABI
7. C header generation or equivalent ABI documentation
8. C# JSON surface matching the canonical wire format
9. a `.NET` package path that is ready to publish to `nuget.org`
10. version synchronization from the shared project version source

## Deferred

1. more advanced ownership-returning APIs
2. allocator-sharing patterns
3. very large automatically generated convenience layers beyond the MVP surface
