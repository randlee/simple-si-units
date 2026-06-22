# Sprint B-5: Phase-End Boundary Hardening

## Status

`Done`

## Scope References

- [Phase B](phase-B-core-quantity-model.md)
- [docs/crates/units-x/requirements.md](../crates/units-x/requirements.md)
- [docs/crates/units-x/architecture.md](../crates/units-x/architecture.md)
- REQ-UX-001
- REQ-UX-002
- REQ-UX-003
- REQ-UX-004
- REQ-UX-009
- REQ-UX-019
- REQ-UX-020
- ADR-UX-013
- ADR-UX-016
- ADR-UX-017

## Goal

Close the Phase B QA gaps without relaxing any existing boundary rules.

## Inputs

- [docs/phase-A/phase-A-findings-1.md](../phase-A/phase-A-findings-1.md)
- phase-ending QA findings on `integration/phase-B`

## Closure

Sprint B-5 closes only when all of the following are true:

1. Scalar quantity storage is catalog-gated at the `Quantity` type boundary and
   the generated public wrappers, constructors, and `QuantityForStorage`
   surface cannot admit unsupported `(unit, storage)` pairs.
2. Bulk quantity storage is sealed so downstream crates cannot extend
   `BulkStorage` or `BulkStorageFor<Unit>` outside the generator-owned impl
   list.
3. The `ffi_contract` module does not expose a public generic quantity alias;
   it remains limited to concrete ABI-oriented exports.
4. Compile-fail coverage proves unsupported scalar storage, unsupported unit
   pairings, and unsupported bulk storage types are rejected at compile time.
5. Generated-artifact tests prove the seal/gate logic is catalog-owned and
   persists across regeneration.

## Implementation Notes

- The scalar gate must be enforced by a sealed trait derived from catalog
  `scalar.type_ids`.
- The bulk gate must preserve the existing public API shape while preventing
  downstream extension.
- Constructor ergonomics such as `Distance::mm(1250_i32)` must remain
  available after the hardening work.

## Required Verification

- `python3 scripts/generate_catalog_artifacts.py`
- `just test`
