# Python Integration PRD

## Purpose

This document defines the Python-facing product requirements for the new unit-preserving quantities crate.

It is intentionally separate from the core PRD because Python has a different object and ABI model than C, C#, Go, and Rust.

## Summary

Python support must provide:

- ergonomic scalar quantity APIs
- efficient array and buffer APIs
- clear JSON interoperability
- compatibility with `maturin` and PyO3 packaging workflows
- generated Pydantic models for every public JSON type
- catalog-driven Python model generation where practical
- a publishable package layout under `python/`

Python support does not need to expose Python objects that are ABI-compatible with the raw C structs used for C#/Go/C/Rust interop.

## Core distinction

There are two different ABI concepts involved:

1. Python extension ABI
   This is the ABI of the compiled Python extension module.
   This can use PyO3 stable ABI support such as `abi3`.

2. Quantity data ABI
   This is the layout of the public quantity structs such as distance, time, velocity, and temperature data.

These are not the same thing.

Python object instances are not required to be blittable or layout-compatible with the raw C ABI quantity structs.

## Goals

### Primary goals

1. Provide a clean Python API for scalar quantities.
2. Provide efficient array and buffer APIs without per-element Python object overhead for bulk data.
3. Support wheel packaging and distribution via `maturin`.
4. Support Python-version-stable extension builds where practical via PyO3 `abi3`.
5. Provide Pydantic models for every public JSON-serializable type used in interop and end-to-end testing.

### Secondary goals

1. Allow a Python path that mirrors the unit-preserving Rust model.
2. Provide a bridge to the same canonical compute logic used by other language bindings.
3. Keep room for future NumPy integration.
4. Avoid hand-maintained drift between Python types and the master unit catalog.

## Non-Goals

1. Making ordinary Python quantity objects blittable POD structs.
2. Requiring Python users to work directly with pointer-plus-length APIs.
3. Forcing Python arrays to be represented as Python object lists when a buffer-based path is possible.

## Integration strategy

The Python deliverable may expose two layers:

1. A high-level PyO3 API for normal Python use
2. Optional lower-level C-ABI access for advanced use through `cffi` or similar approaches if needed

The high-level API is the primary product surface.

## Repository Layout

The Python production package must live under `python/`.

Recommended shape:

- `python/<package>/` for the importable production package
- `python/<package>/models/` for stable model exports
- `python/<package>/models/generated/` for generated Pydantic model implementations
- `python/tests/` for Python-facing tests

Generated models may be regenerated freely, but the public import surface should remain stable.

## Packaging Requirements

The Python package must support:

- `maturin`
- PyO3 bindings
- stable Python extension ABI where appropriate using `abi3`
- `pip install` from the repository and from built distributions
- publication to PyPI when release processes are enabled

This stable ABI support is about Python wheel compatibility, not quantity struct layout compatibility.

The Python package version must come from the shared project version source of truth, not from an independently edited Python-only version string.

## Scalar API Requirements

Python scalar quantities must be easy to construct and convert.

Examples of intended shape:

- `Distance.mm(1250)`
- `Distance.cm(12.5)`
- `Distance.ft(6.0)`
- `Temperature.degC(25.0)`
- `Temperature.degF(77.0)`

Required capabilities:

1. Construction from explicit unit-specific constructors
2. Accessors for explicit unit-specific views
3. Clear string representation
4. JSON-friendly conversion
5. Bridge to canonical compute operations

Example desired usage:

```python
d = Distance.mm(1250)
t = Time.s(2.0)
v = d.velocity_over(t)
assert abs(v.mps() - 0.625) < 1e-12
```

## Bulk Data Requirements

Python bulk data must avoid per-element object overhead wherever possible.

Preferred mechanisms:

- Python buffer protocol
- `memoryview`
- `bytes` or `bytearray` where appropriate
- optional NumPy-compatible paths later

Array and buffer APIs should operate over raw numeric storage with explicit unit metadata.

Examples of desired shapes:

- `DistanceArray.mm_i32(memoryview_or_buffer)`
- `DistanceArray.cm_f32(...)`
- `TemperatureArray.degC_f32(...)`

## JSON Requirements

Python APIs must support clean JSON serialization and deserialization.

Recommended scalar shape:

```json
{
  "type": "distance_i32",
  "unit": "mm",
  "value": 1250
}
```

Recommended fixed small-array shape:

```json
{
  "type": "distance3_f32",
  "unit": "cm",
  "values": [12.0, 15.0, 18.0]
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

Python requirements:

1. JSON should always include explicit unit metadata
2. JSON should not depend on implicit Rust field names
3. JSON round-trip tests must be part of validation
4. A Pydantic model must exist for every public JSON shape
5. Pydantic serialization output must match the canonical cross-language wire shape semantically against shared fixtures
6. Human-readable unit symbols such as `C` may differ from safe code identifiers such as `degC`

Canonical JSON policy for Python:

- scalars use the compact `type` + `unit` + `value` shape
- fixed small buffers may use JSON arrays
- large or arbitrary buffers use encoded payload envelopes
- the chosen JSON form is a machine-readable property of the public type, not a runtime serializer heuristic
- non-finite floating-point values are out of scope for canonical JSON unless a later explicit policy is added

## Pydantic Requirements

The project must generate or maintain Pydantic models for every public JSON-serializable scalar and bulk quantity type.

Requirements:

1. Models must use the same field names and shape as the canonical Rust JSON schema.
2. Models must support end-to-end interop tests against Rust and C#.
3. Model generation should preferably be schema-driven rather than hand-maintained where practical.
4. Pydantic round-trip behavior must be included in validation.
5. The model set should be regenerable when the master catalog changes.
6. Generated Pydantic models should live under the production package tree so they ship with the installed package.

## Binary/Bulk Buffer Requirements

For Python bulk data, the preferred efficient path is not a Python object per quantity. It is raw typed buffers with unit metadata handled at the container or API layer.

Requirements:

1. Arrays should be exposable as contiguous numeric buffers
2. Unit metadata should live at the container or schema level
3. Python users should be able to consume arrays without copying when feasible

## Relationship to raw C ABI

Python high-level objects do not need to match the raw C ABI quantity struct layout.

However:

- the Python implementation may internally call the same Rust core logic
- Python may consume the same binary wire-format semantics for arrays and buffers
- advanced Python integrations may expose or consume the raw C ABI through separate mechanisms if needed
- the primary Python bulk API is still PyO3-native and buffer-oriented rather than a direct projection of pointer-plus-length ABI structs
- Python JSON DTOs and buffer-facing APIs target the wire/raw-numeric representation, not the in-memory ABI wrapper layout

## Validation Requirements

Python support must include:

1. wheel build validation with `maturin`
2. JSON round-trip tests
3. scalar conversion tests
4. array and buffer API tests
5. parity tests against the Rust core behavior
6. Pydantic serialization parity tests against the canonical JSON fixtures

## V1 Scope

V1 must include:

1. `maturin`-based packaging
2. PyO3 scalar quantity API
3. explicit unit constructors and accessors
4. bulk buffer support for arrays
5. JSON-friendly serialization surface
6. distance, time, temperature, velocity, and acceleration support
7. Celsius and Fahrenheit support
8. Pydantic models for every public JSON type
9. a package layout under `python/` that is ready for PyPI/pip distribution
10. version synchronization with the shared project version source

## Deferred

1. full NumPy-first API design
2. pandas-specific integration
3. full low-level `cffi` product surface unless it becomes necessary
