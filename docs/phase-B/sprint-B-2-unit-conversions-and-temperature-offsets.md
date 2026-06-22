# Sprint B-2: Unit Conversions And Temperature Offsets

## Goal

Implement conversion logic for multiplicative units and MVP offset-temperature units.

## Status

`Not Started`

## Scope References

- REQ-UX-006
- REQ-UX-007
- REQ-UX-008
- REQ-UX-009
- REQ-UX-011
- REQ-UX-035
- REQ-UX-041
- REQ-UX-025
- REQ-UX-029
- REQ-UX-034
- REQ-UX-040
- REQ-UX-042
- REQ-UX-043
- REQ-UX-044
- REQ-UX-045
- REQ-UX-046
- ADR-UX-003
- ADR-UX-010
- ADR-UX-017
- ADR-UX-019
- ADR-UX-020
- ADR-UX-021
- ADR-UX-022

## Deliverables

1. Multiplicative conversions for the in-scope `base`, `geometry`, `mechanical`, and `electromagnetic` unit families
2. Celsius, Fahrenheit, and Kelvin conversion logic
3. Canonical-dimension-driven compatibility for reciprocal public quantities,
   including `Diopter`
4. Catalog-owned conversion tables and runtime metadata derived from
   `catalog/units-catalog.json`
5. Conversion-coverage completion for every public type row in
   `catalog/generated/units-catalog-summary.json`
6. Reference-source parity fixtures or tests that validate the catalog without
   replacing it as the source of truth
7. Generated conversion-coverage report at
   `catalog/generated/phase-b-conversion-coverage.json`
8. Stable `ConversionError` contract for all fallible conversion paths

## Dependencies

- Sprint A-6
- Sprint B-1

## Unblocks

- Sprints B-3, C-1, E-1

## Out Of Scope

- mixed-unit arithmetic semantics and canonical compute bridges, which close in
  Sprint B-3
- JSON DTO shape, binary envelope shape, and stable ABI-facing boundary types,
  which close in later phases

## Acceptance Criteria

1. Multiplicative conversions are implemented for the in-scope unit families.
2. Celsius, Fahrenheit, and Kelvin conversion rules are explicit and correct.
3. Same-canonical-dimension public units such as `Diopter` and
   `InverseDistance` are explicitly supported without collapsing their public
   identities.
4. Conversion execution derives from the committed catalog and generated
   metadata; reference-project sources may validate parity but may not become a
   second runtime source of truth.
5. The crate can represent the planned distance examples `mm`, `m`, and `ft`.
6. Potentially lossy storage conversions are routed through explicit fallible APIs.
7. The sprint cannot close while any in-scope conversion path lacks a documented
   status row in the authoritative matrix for this sprint.
8. `catalog/generated/phase-b-conversion-coverage.json` is the authoritative
   closure artifact for per-conversion-path status and contains exactly one row
   per supported or intentionally unsupported conversion path in scope.
9. Same-public-type unit conversion, same-canonical-dimension cross-public-type
   conversion, and reciprocal-domain conversion each have one explicit result
   identity rule and one authoritative API boundary.
10. `ConversionError` variants and triggering conditions are fixed by the sprint
    doc rather than inferred from examples.
11. Conversion paths that are marked fallible in the authoritative matrix do not
    expose the infallible unit-conversion API.

## Required Validation

1. Dedicated round-trip tests cover `mm -> m -> mm` and `ft -> m -> ft`.
2. Dedicated temperature tests cover negative values and offset-sensitive values such as freezing/boiling points.
3. Mixed conversion tests verify symbol/id handling does not confuse `C`/`degC`.
4. Dedicated tests cover a lossy integer-backed conversion failure path.
5. Dedicated tests cover `Diopter::dpt(2.0) <-> InverseDistance::per_m(2.0)`
   and prove same-canonical-dimension compatibility is keyed by
   `canonical_dimension_id`.
6. Dedicated tests cover `Distance::m(0.5) <-> Diopter::dpt(2.0)` as a
   reciprocal-domain bridge that does not rely on canonical-dimension
   equality.
7. Regeneration or parity validation confirms conversion tables and unit ids are
   derived from the catalog without manual drift.
8. Validation proves conversion paths marked `try_to_unit`-only or
   bridge-only do not expose the infallible unit-conversion API.
9. Validation records conversion support status for every item in the
   authoritative inventory.
10. Validation confirms `catalog/generated/phase-b-conversion-coverage.json`
   contains one row per in-scope conversion path with explicit support status,
   path kind, and expected failure class when the path is fallible or
   unsupported.
11. Dedicated tests cover every declared `ConversionError` variant directly.

## Edge / Corner Conditions Requiring Dedicated Tests

1. Offset-temperature conversions where both scale and offset matter.
2. Negative temperature values.
3. Cross-system conversion between imperial and metric units.
4. Reciprocal-domain conversions between distance and diopter.
5. Distinct public types that share a `canonical_dimension_id`.
6. Reciprocal-domain conversions between public types with different canonical
   dimensions.

## Code Samples / Contracts

Representative API shape:

```rust
let distance = Distance::mm(1250.0);
let meters = distance.to_unit::<m>();

let freezing = Temperature::degC(0.0);
let fahrenheit = freezing.to_unit::<degF>();
assert_eq!(fahrenheit.value(), 32.0);

let focus = Distance::m(0.5).to_reciprocal_quantity::<Diopter>()?;
assert_eq!(focus.value(), 2.0);

let exact = Distance::mm(1000_i32).try_to_unit::<m, i32>()?;
let lossy = Distance::mm(1_i32).try_to_unit::<m, i32>();
assert!(lossy.is_err());
```

Conversion-path rule:

- `to` is only valid for conversion paths whose source-storage and
  destination-storage pair is documented as structurally infallible for all
  values representable by the source type.
- `try_to` is required whenever exactness depends on the runtime value or when
  storage overflow, truncation, or precision loss is otherwise possible for the
  destination type.

Representative infallible and fallible examples:

```rust
let infallible = Distance::mm(1250.0_f64).to_unit::<m>();
assert_eq!(infallible.value(), 1.25);

let exact = Distance::mm(1000_i32).try_to_unit::<m, i32>()?;
assert_eq!(exact.value(), 1);

let precision_loss = Distance::mm(1_i32).try_to_unit::<m, i32>();
assert!(matches!(precision_loss, Err(ConversionError::PrecisionLoss)));

let overflow = Distance::km(i64::MAX).try_to_unit::<mm, i32>();
assert!(matches!(overflow, Err(ConversionError::Overflow)));
```

Authoritative conversion-boundary contract:

```rust
pub trait ConvertUnit<TargetUnit> {
    type Output;

    fn to_unit(self) -> Self::Output;
}

pub trait TryConvertUnit<TargetUnit, TargetStorage> {
    type Output;

    fn try_to_unit(self) -> Result<Self::Output, ConversionError>;
}

pub trait TryConvertQuantity<TargetQuantity, TargetUnit, TargetStorage> {
    fn try_to_quantity(self) -> Result<TargetQuantity, ConversionError>;
}

pub trait ReciprocalBridge<TargetQuantity> {
    fn to_reciprocal_quantity(self) -> Result<TargetQuantity, ConversionError>;
}
```

Result-identity rule:

- same-public-type unit conversion is selected by target unit and preserves the
  source public quantity type plus source storage type
- same-public-type storage-changing conversion is selected by target unit and
  explicit target storage type
- same-canonical-dimension cross-public-type conversion is selected by explicit
  target public quantity type, explicit target unit, and explicit target
  storage type
- reciprocal-domain conversion such as `Distance <-> Diopter` uses a dedicated
  bridge API and never reuses same-dimension unit-conversion dispatch
- paths marked `try_to_unit`-only in the authoritative matrix must not expose
  `ConvertUnit<TargetUnit>`

Representative public-identity examples:

```rust
let meters: Distance = Distance::mm(1250.0).to_unit::<m>();
let inverse: InverseDistance =
    Diopter::dpt(2.0).try_to_quantity::<InverseDistance, per_m, f64>()?;
let focus: Diopter = Distance::m(0.5).to_reciprocal_quantity::<Diopter>()?;
```

Stable `ConversionError` contract:

```rust
pub enum ConversionError {
    IncompatibleCanonicalDimension,
    UnsupportedBridge,
    MissingCatalogPath,
    DomainViolation,
    Overflow,
    PrecisionLoss,
}
```

Error-variant rules:

- `IncompatibleCanonicalDimension`: same-dimension conversion API was asked to
  cross unrelated canonical dimensions
- `UnsupportedBridge`: caller requested a cross-dimension conversion outside the
  documented reciprocal-domain bridge set
- `MissingCatalogPath`: the catalog does not define the requested same-dimension
  unit or public-type conversion path
- `DomainViolation`: the documented bridge is mathematically undefined for the
  runtime value, for example zero distance into diopter
- `Overflow`: destination storage cannot represent the converted value
- `PrecisionLoss`: destination storage would lose required precision

Authoritative conversion-coverage artifact columns:

- `source_public_type`
- `source_unit`
- `source_storage`
- `target_public_type`
- `target_unit`
- `target_storage`
- `path_kind`
- `api_surface`
- `support_status`
- `expected_failure`

## Closure Gate

The authoritative public-type coverage gate for this sprint is
`catalog/generated/units-catalog-summary.json`.
This sprint does not close until the authoritative
per-conversion-path matrix in `catalog/generated/phase-b-conversion-coverage.json`
enumerates every supported or intentionally unsupported path exactly once.
