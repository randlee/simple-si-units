# Phase C Findings 1

## Scope

Reviewed:

- [Phase C overview](phase-C-serialization-and-binary-contract.md)
- [Sprint C-1](sprint-C-1-json-schema-and-serde-surface.md)
- [Sprint C-2](sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md)
- [Sprint C-3](sprint-C-3-layout-endianness-and-conformance-tests.md)

Against:

- [docs/crates/units-x/requirements.md](../crates/units-x/requirements.md)
- [docs/crates/units-x/architecture.md](../crates/units-x/architecture.md)
- implemented Phase B core in `crates/units-x`
- catalog-derived metadata under `catalog/generated/`

## Findings

### 1. Binary envelope fields conflict with the current catalog-owned identifier model

Severity: `High`

- [docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:46](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:46>)
- [docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:62](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:62>)
- [docs/crates/units-x/requirements.md:113](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/crates/units-x/requirements.md:113>)
- [docs/crates/units-x/requirements.md:144](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/crates/units-x/requirements.md:144>)
- [docs/crates/units-x/architecture.md:254](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/crates/units-x/architecture.md:254>)
- [docs/crates/units-x/architecture.md:387](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/crates/units-x/architecture.md:387>)
- [crates/units-x/src/generated/catalog_metadata.rs:31](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/generated/catalog_metadata.rs:31>)
- [crates/units-x/src/generated/catalog_metadata.rs:83](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/generated/catalog_metadata.rs:83>)
- [catalog/units-catalog.json:627](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/catalog/units-catalog.json:627>)

Sprint C-2 currently specifies numeric `type_id` and `unit_id` fields. The
implemented catalog model already publishes binary identifiers as deterministic
strings such as `units-x.distance.v1` and `distance.mm`. As written, the sprint
would introduce a second identifier registry that is not catalog-owned.

### 2. The zero-copy story is not reconciled with the existing ABI and typed bulk surfaces

Severity: `High`

- [docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:5](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:5>)
- [docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:49](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:49>)
- [crates/units-x/src/bulk.rs:60](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/bulk.rs:60>)
- [crates/units-x/src/bulk.rs:71](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/bulk.rs:71>)
- [crates/units-x/src/bulk.rs:82](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/bulk.rs:82>)
- [crates/units-x/src/ffi_contract.rs:11](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/ffi_contract.rs:11>)
- [crates/units-x/src/ffi_contract.rs:31](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/ffi_contract.rs:31>)
- [docs/crates/units-x/architecture.md:115](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/crates/units-x/architecture.md:115>)

Phase B already established three distinct bulk shapes in Rust and a separate
ABI ownership/status model. Sprint C-2 says "zero-copy" but does not define
whether that means byte-level borrowing, typed element borrowing on
little-endian hosts only, or a separate borrowed-envelope API. That ambiguity
is large enough to produce incompatible implementations later in Phase D/E.

### 3. Sprint C-1 contains wire examples that do not match the current catalog

Severity: `High`

- [docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:72](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:72>)
- [docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:82](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:82>)
- [catalog/generated/units-catalog-summary.json:609](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/catalog/generated/units-catalog-summary.json:609>)
- [catalog/generated/units-catalog-summary.json:610](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/catalog/generated/units-catalog-summary.json:610>)
- [catalog/generated/units-catalog-summary.json:611](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/catalog/generated/units-catalog-summary.json:611>)
- [crates/units-x/src/generated/catalog_metadata.rs:39](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/generated/catalog_metadata.rs:39>)

Two sample-level drifts exist today:

- the fixed-array example uses unit `cm`, but the current `Distance` catalog
  only publishes `mm`, `m`, and `ft`
- the encoded-buffer example uses `encoding: "base64-le-f32"`, while the
  catalog-owned encoding vocabulary is currently `object`, `array`, and
  `base64-le`

These examples would mislead fixture and test authors if left unchanged.

### 4. Phase C dependencies do not fully reflect the completed Phase B implementation

Severity: `Medium`

- [docs/phase-C/phase-C-serialization-and-binary-contract.md:41](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/phase-C-serialization-and-binary-contract.md:41>)
- [docs/phase-C/phase-C-serialization-and-binary-contract.md:42](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/phase-C-serialization-and-binary-contract.md:42>)
- [docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:37](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:37>)
- [docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:36](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md:36>)
- [docs/phase-B/sprint-B-4-array-and-buffer-quantity-model.md:55](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-B/sprint-B-4-array-and-buffer-quantity-model.md:55>)
- [docs/phase-B/sprint-B-5-phase-end-boundary-hardening.md:27](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-B/sprint-B-5-phase-end-boundary-hardening.md:27>)
- [crates/units-x/src/bulk.rs:235](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/bulk.rs:235>)

C-1 depends on bulk classification and public bulk shapes from B-4, but B-4 is
missing from its dependency list. C-2 depends on the hardened generator-owned
metadata and boundary model from B-5, but that prerequisite is also implicit.
The current dependency graph understates the amount of Phase B surface that
Phase C actually builds on.

### 5. C-1 does not say what happens for borrowed bulk views during serde

Severity: `Medium`

- [docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:28](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:28>)
- [docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:55](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:55>)
- [crates/units-x/src/bulk.rs:82](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/bulk.rs:82>)

`QuantityBufferView<'a, Unit, T>` is part of the Phase B public Rust bulk
surface, but C-1 never states whether borrowed views are serialize-only,
round-trippable through an owned DTO, or out-of-scope for deserialization.
That policy needs to be explicit before implementation starts.

### 6. C-1 validation is too loose for distinct public types that share one canonical dimension

Severity: `Medium`

- [docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:56](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-1-json-schema-and-serde-surface.md:56>)
- [docs/phase-B/sprint-B-2-unit-conversions-and-temperature-offsets.md:73](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-B/sprint-B-2-unit-conversions-and-temperature-offsets.md:73>)
- [crates/units-x/src/generated/public_types.rs:20405](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/generated/public_types.rs:20405>)
- [crates/units-x/src/generated/public_types.rs:20923](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/generated/public_types.rs:20923>)

The current validation language only mentions mismatched `type` and `unit`
pairs. It does not explicitly protect distinct public identities such as
`Diopter` and `InverseDistance`, which share one `canonical_dimension_id` but
must remain different JSON types.

### 7. C-3 scope and validation blur ABI layout checks with binary-wire conformance

Severity: `High`

- [docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:5](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:5>)
- [docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:11](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:11>)
- [docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:48](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:48>)
- [docs/crates/units-x/requirements.md:90](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/crates/units-x/requirements.md:90>)
- [docs/crates/units-x/architecture.md:115](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/crates/units-x/architecture.md:115>)
- [crates/units-x/src/ffi_contract.rs:12](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/ffi_contract.rs:12>)
- [crates/units-x/src/ffi_contract.rs:149](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/ffi_contract.rs:149>)

C-3 currently mixes:

- ABI struct layout tests
- JSON fixture drift tests
- binary-envelope conformance tests

Those are related, but they are not the same contract. As written, the sprint
could close with `repr(C)` layout coverage while still leaving the actual
binary envelope contract under-tested.

### 8. C-3 validation language is too weak for the already-shipped ABI boundary

Severity: `Medium`

- [docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:48](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:48>)
- [docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:49](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/docs/phase-C/sprint-C-3-layout-endianness-and-conformance-tests.md:49>)
- [crates/units-x/src/ffi_contract.rs:14](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/ffi_contract.rs:14>)
- [crates/units-x/src/ffi_contract.rs:34](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/ffi_contract.rs:34>)
- [crates/units-x/src/ffi_contract.rs:117](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/ffi_contract.rs:117>)
- [crates/units-x/src/ffi_contract.rs:189](</Volumes/Extreme Pro/github/simple-si-units-worktrees/planning/phase-C/crates/units-x/src/ffi_contract.rs:189>)

Phrases such as "where available" and "at least one scalar and one buffer
case" are not strong enough now that the repo already ships concrete ABI
invariants around `u64` lengths, null-plus-zero semantics, status-code width,
overflow codes, and owned-buffer destruction. The sprint should require those
checks explicitly.

## Summary

The main issues are contract drift and underspecification, not missing
motivation. Phase B already established real catalog metadata, typed bulk
surfaces, and ABI rules. Phase C needs to be rewritten so it builds from those
artifacts directly instead of inventing a parallel binary-id model or leaving
serde/buffer behavior open to interpretation.
