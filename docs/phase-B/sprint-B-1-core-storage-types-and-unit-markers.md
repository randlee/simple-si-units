# Sprint B-1: Core Storage Types And Unit Markers

## Goal

Implement the primary scalar quantity container and the full in-scope public
scalar type set.

## Status

`Complete`

## Scope References

- REQ-UX-001
- REQ-UX-002
- REQ-UX-005
- REQ-UX-009
- REQ-UX-011
- REQ-UX-029
- REQ-UX-034
- REQ-UX-040
- REQ-UX-042
- REQ-UX-043
- REQ-UX-044
- NFR-UX-001
- NFR-UX-013
- ADR-UX-002
- ADR-UX-003
- ADR-UX-017
- ADR-UX-020
- ADR-UX-021

## Deliverables

1. Core transparent quantity container separating unit marker and storage payload
2. Foundational unit marker traits
3. Public type definitions for every catalog-defined public type in
   `catalog/generated/units-catalog-summary.json`
4. `Diopter` public type mapped to the inverse-distance dimension
5. Size assertions demonstrating zero additional storage overhead
6. Catalog-metadata-backed type/unit generation or parity checks for the public
   scalar surface
7. Sealed unit-marker trait contract for catalog-derived public units

## Dependencies

- Sprint A-6

## Unblocks

- Sprints B-2, B-3, B-4

## Out Of Scope

- fixed-size array wrappers and variable-length bulk wrappers, which close in
  Sprint B-4
- conversion behavior, arithmetic behavior, JSON shape, binary shape, and ABI
  shape, which close in later sprints and phases

## Acceptance Criteria

1. The primary quantity container shape is implemented with explicit unit marker and storage payload separation.
2. Foundational unit markers exist for every public type and unit row captured
   by the authoritative catalog-derived summary.
3. Scalar wrappers demonstrate zero additional storage overhead over their payloads.
4. Unit marker naming rules are enforceable in code for case-sensitive units.
5. No in-scope type may be omitted from closure on the basis that its family was “implicitly covered.”
6. The implemented public scalar surface is generated from or mechanically
   checked against the authoritative Phase A generated artifacts
   `catalog/generated/units-catalog-summary.json` and
   `crates/units-x/src/generated/catalog_metadata.rs`.
7. The unit-marker contract explicitly defines the metadata exposed to later
   conversion and arithmetic work and whether external crates may implement the
   marker traits.

## Required Validation

1. `size_of::<Quantity<mm, i32>>() == size_of::<i32>()` test exists.
2. Dedicated type-level tests distinguish `mm` from `Mm`.
3. Dedicated type-level tests cover `degC` and `degF` naming.
4. Validation references the authoritative catalog-derived summary and confirms
   every in-scope public type in this sprint is implemented exactly once.
5. Regeneration or parity validation confirms the implemented public scalar
   surface matches `catalog/generated/units-catalog-summary.json` and
   `crates/units-x/src/generated/catalog_metadata.rs` without drift.

## Code Samples / Contracts

Representative container:

```rust
#[repr(transparent)]
pub struct Quantity<Unit, Storage> {
    pub storage: Storage,
    _unit: core::marker::PhantomData<Unit>,
}
```

Representative marker-trait contract:

```rust
mod private {
    pub trait SealedUnit {}
}

pub trait UnitMarker: private::SealedUnit + Copy + 'static {
    const UNIT_SYMBOL: &'static str;
    const UNIT_CODE_ID: &'static str;
    const DIMENSION_ID: &'static str;
    const CANONICAL_DIMENSION_ID: &'static str;
}
```

## Closure Gate

The authoritative public-type coverage gate for this sprint is
`catalog/generated/units-catalog-summary.json`.
This sprint does not close until every public type row in that summary is
implemented and the resulting scalar surface matches
`catalog/generated/units-catalog-summary.json` for public type and unit
coverage plus `crates/units-x/src/generated/catalog_metadata.rs` for
Rust-consumable catalog metadata parity. The markdown inventory checklist is a
derived review aid and must remain in parity without becoming a second source
of truth.
