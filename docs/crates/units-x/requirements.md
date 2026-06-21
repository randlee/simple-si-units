# units-x Crate Requirements

## Scope

This document contains the numbered functional and non-functional requirements
for the primary `units-x` Rust crate.

All design docs, sprint docs, and implementation planning docs that affect the
crate should cite these ids directly.

Detailed product narrative remains in the PRDs. This file is the traceable
crate-level requirement surface.

## Requirement Groups

- Quantity model
- Unit catalog and conversion model
- Serialization
- ABI / interop support
- Arithmetic and compute bridges
- Tooling, generation, and validation

## Functional Requirements

### Quantity Model

#### REQ-UX-001

The crate must provide unit-preserving quantity types rather than only
canonical-SI-internal public storage types.

#### REQ-UX-002

The crate must support scalar quantities.

#### REQ-UX-003

The crate must support fixed-size array/buffer-oriented quantity forms.

#### REQ-UX-004

The crate must support variable-length buffer-oriented quantity forms where the
selected API surface requires them.

#### REQ-UX-005

The public quantity model must retain explicit unit identity for a stored value
or buffer.

### Unit Catalog And Conversion

#### REQ-UX-006

The crate must support explicit conversion between supported units using
catalog-defined conversion metadata.

#### REQ-UX-007

The crate must support non-SI units in addition to SI units.

#### REQ-UX-008

The crate must support temperature units in the MVP, including Celsius and
Fahrenheit.

#### REQ-UX-009

The crate must derive unit/type surfaces from the master catalog rather than
requiring broad duplicated manual definitions.

#### REQ-UX-010

The crate must support human-readable unit symbols and separate code-safe unit
identifiers where those differ.

#### REQ-UX-011

The crate must support the V1 unit-family scope discussed in planning:

- every public type listed in
  [in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md)

### Serialization

#### REQ-UX-012

The crate must provide a documented JSON serialization path for public quantity
types.

#### REQ-UX-013

The crate must provide a documented binary serialization path distinct from the
in-memory ABI representation.

#### REQ-UX-014

The crate must support compact scalar JSON forms using explicit type and unit
metadata.

#### REQ-UX-015

The crate must support explicit JSON handling for fixed small buffers.

#### REQ-UX-016

The crate must support explicit JSON handling for large or arbitrary buffers.

#### REQ-UX-017

The crate must define a machine-readable classification of which public types
use inline JSON arrays versus encoded-buffer JSON envelopes.

#### REQ-UX-018

The crate must define a binary-safe unit-id namespace suitable for wire
contracts and generated interop artifacts.

#### REQ-UX-033

The canonical JSON contract for every public type must be consumable without
shape drift by Rust serde, generated Python Pydantic models, and C#
`System.Text.Json` support.

#### REQ-UX-034

The master catalog must be stored in-repo as a machine-readable JSON document
that acts as a source-of-truth generation input.

#### REQ-UX-035

The master catalog and conversion model must represent both multiplicative and
affine conversions, including temperature offset metadata.

#### REQ-UX-036

Public JSON wire contracts must use human-readable unit symbols such as `mm`,
`ft`, `C`, and `F` rather than code-safe identifiers such as `degC`.

#### REQ-UX-039

The binary wire contract must fix endianness, field widths, schema-level unit
metadata rules, and unknown-version handling.

#### REQ-UX-040

JSON type ids, binary unit ids, and ABI type names must follow deterministic
catalog-derived naming schemes.

### ABI / Interop

#### REQ-UX-019

The crate must expose or support stable C-ABI-facing concrete types for
foreign-language interop.

#### REQ-UX-020

The crate must support monomorphic ABI-facing scalar quantity types.

#### REQ-UX-021

The crate must support ABI-safe slice or buffer views using explicit
pointer-plus-length contracts with documented mutability and ownership rules.

#### REQ-UX-022

The crate must define an explicit ABI status/error model for slice and buffer
operations that can fail.
Caller-provided output pointers and Rust-owned output buffers must have distinct
documented failure codes rather than relying on implicit null-pointer behavior.

#### REQ-UX-037

The ABI contract must define valid empty-slice semantics, including the
behavior of `null` pointer plus zero length and rejection of `null` pointer
plus non-zero length.

#### REQ-UX-038

The ABI contract must define ownership, lifetime, and destroy-function rules
for borrowed inputs and any owned outputs.

### Arithmetic And Compute Bridges

#### REQ-UX-023

The crate must support canonical compute bridges used for derivative
calculations such as velocity and acceleration.

#### REQ-UX-024

The crate must support conversion from unit-preserving stored forms into
compute-friendly canonical forms when arithmetic requires it.

#### REQ-UX-025

The crate must support the distance-related examples discussed in planning,
including `m`, `mm`, and `ft`.

#### REQ-UX-042

The crate must support the reference-project unit families `base`, `geometry`,
`mechanical`, and `electromagnetic` in the MVP catalog and generated public
surfaces.

#### REQ-UX-043

The crate must support public reciprocal quantities when they correspond to
real domain units rather than only algebra artifacts.

#### REQ-UX-044

The crate must support `Diopter` as a first-class public quantity mapped to
the inverse-distance dimension, including conversion compatibility with
distance.

#### REQ-UX-045

The MVP is not required to reproduce the full legacy operator graph for every
possible unit combination, but it must support conversion, serialization, and
documented derived operations across the in-scope unit families.

#### REQ-UX-026

The crate must support the derivative chain from distance to velocity to
acceleration in the MVP architecture.

#### REQ-UX-027

The crate must support mixed-unit addition and subtraction with documented
unit-preservation rules.

#### REQ-UX-028

The crate must support deterministic mixed-storage promotion rules for
cross-unit arithmetic.

#### REQ-UX-041

Potentially lossy or overflow-prone storage conversions must use explicit
fallible APIs rather than silently truncating data.

### Tooling, Generation, And Validation

#### REQ-UX-029

The crate must be generation-friendly so that new units can be added primarily
through catalog edits and regeneration.

#### REQ-UX-030

The crate must be publishable under the repo’s shared version source-of-truth
model.

#### REQ-UX-031

The crate must be covered by repository validation paths that include
generation, version-lock verification, linting, and testing.

#### REQ-UX-032

The crate must participate in canonical JSON and binary fixture generation or
ownership for downstream language parity testing.

## Non-Functional Requirements

### Footprint And Layout

#### NFR-UX-001

Scalar quantity wrappers and fixed-size array quantity wrappers must match the
footprint of their underlying payload storage exactly. Variable-length buffer
views may add only the metadata fields required by the chosen Rust or ABI
boundary contract.

#### NFR-UX-002

The design must avoid per-element wrapper overhead for contiguous array/buffer
payloads.

#### NFR-UX-003

Public interop-facing layouts must be cross-platform stable and explicitly
documented.

#### NFR-UX-004

ABI-facing slice and buffer contracts must avoid platform-dependent width
choices at the stable boundary.

### Determinism And Compatibility

#### NFR-UX-005

Serialization behavior must be deterministic across supported platforms and
languages.

#### NFR-UX-006

The crate must avoid hidden platform assumptions such as implicit text
encodings or hardcoded Unix-only runtime paths in generation and support code.

#### NFR-UX-007

The crate’s public contract surface must remain suitable for Rust, C, C#, Go,
and Python integration as scoped by the PRDs.

### Extensibility And Maintenance

#### NFR-UX-008

The crate design must remain extensible so that adding units primarily means
editing the master catalog and regenerating artifacts.

#### NFR-UX-009

The crate should minimize hand-maintained duplication of unit metadata across
Rust, Python, C#, Go, and tests.

#### NFR-UX-010

Requirement ids and public contract names must remain stable enough for
planning, QA, and design traceability.

### Release And Validation

#### NFR-UX-011

The crate must be suitable for publication and version synchronization under
the repo’s shared version source-of-truth model.

#### NFR-UX-012

The crate must remain compatible with the repository’s cross-platform CI and
local `just` workflow expectations.

#### NFR-UX-013

The crate’s catalog, JSON contract, and binary contract should be
machine-readable enough to drive downstream generation and conformance tests.

## Traceability Notes

- Product-wide narrative and rationale remain in the PRDs.
- Crate-local ADRs are defined in
  [architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/architecture.md).
- Sprint and design docs should cite the smallest relevant set of ids rather
  than copying requirement prose inline.
