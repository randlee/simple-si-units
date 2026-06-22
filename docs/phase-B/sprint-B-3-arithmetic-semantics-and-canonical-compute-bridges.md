# Sprint B-3: Arithmetic Semantics And Canonical Compute Bridges

## Goal

Define and implement scalar arithmetic, mixed-unit addition/subtraction, and bridges to canonical compute outputs for derived calculations.

## Status

`Not Started`

## Scope References

- REQ-UX-023
- REQ-UX-024
- REQ-UX-025
- REQ-UX-026
- REQ-UX-027
- REQ-UX-028
- REQ-UX-043
- REQ-UX-044
- REQ-UX-041
- REQ-UX-046
- REQ-UX-045
- ADR-UX-013
- ADR-UX-019
- ADR-UX-022

## Deliverables

1. Same-canonical-dimension scalar multiply-by-scalar and divide-by-scalar
   semantics across the authoritative inventory
2. Same-canonical-dimension mixed-unit addition and subtraction with
   left-hand-unit preservation across the authoritative inventory
3. Deterministic mixed-storage promotion rules
4. Canonical compute bridges for velocity and acceleration calculations
5. Explicit non-support boundary for the legacy cross-dimension operator graph beyond the documented bridge set
6. Inventory-backed arithmetic support matrix covering every in-scope public
   type, with any exclusions named explicitly
7. Generated arithmetic support matrix at
   `catalog/generated/phase-b-arithmetic-support.json`
8. Stable `ArithmeticError` and `ComputeError` contracts for fallible runtime
   paths in this sprint

## Dependencies

- Sprint A-6
- Sprint B-1
- Sprint B-2

## Unblocks

- Sprints D-1, E-1, F-1

## Parallelism

- Sprint B-4 may run in parallel after Sprint B-1 because it does not depend on
  Sprint B-2
- Sprint B-4 does not block B-3 closure, but Sprint B-3 may not start before
  Sprint B-2 closes

## Out Of Scope

- reopening the catalog conversion tables from Sprint B-2
- reconstruction of the full legacy cross-dimension operator graph beyond the
  documented V1 compute bridges
- arithmetic on absolute temperature quantities in `degC`, `degF`, and `K`,
  which is intentionally unsupported in V1 and must be recorded as such in the
  authoritative arithmetic matrix
- stable ABI function signatures and language-wrapper ergonomics, which close
  in later phases

## Acceptance Criteria

1. Multiplication and division by unitless scalars preserve the declared unit
   across the authoritative inventory.
2. Mixed-unit addition and subtraction use one documented unit-preservation rule
   across the authoritative inventory.
3. Mixed-storage arithmetic uses one documented promotion rule.
4. Derived calculations are limited to the documented canonical set rather than open-ended combinatorial result typing.
5. The sprint explicitly states which arithmetic is intentionally unsupported in V1 instead of leaving gaps for inference.
6. Same-dimension compatibility is determined from catalog
   `canonical_dimension_id`, not from public-type-name equality.
7. The mixed-storage promotion rule names the promoted result type for every
   supported scalar arithmetic path in this sprint.
8. Same-canonical-dimension arithmetic across distinct public types preserves
   the left-hand public quantity identity unless the path is named unsupported
   in the authoritative matrix.
9. `ArithmeticError` and `ComputeError` variants and triggering conditions are
   fixed by the sprint doc rather than inferred from examples.
10. Absolute-temperature arithmetic paths are recorded as intentionally
    unsupported in V1 unless a later ADR changes that boundary.
11. Unsupported type pairs and unsupported storage pairs are represented by
    compile-time absence from the arithmetic API surface and by explicit
    non-support rows in the authoritative matrix, not by runtime error variants.
12. Integer add/subtract/multiply paths that can overflow in the selected
    result storage use checked APIs and `ArithmeticError::Overflow` unless the
    authoritative matrix widens the result storage enough to make the path
    infallible.

## Required Validation

1. Dedicated tests cover `distance_cm + distance_m` with documented left-hand preservation behavior.
2. Dedicated tests cover mixed integer/float storage promotion.
3. Dedicated tests cover the distance -> velocity -> acceleration chain.
4. Dedicated tests cover zero-duration rejection or failure behavior for velocity/acceleration compute bridges.
5. Dedicated tests cover arithmetic compatibility between `InverseDistance` and
   `Diopter` while preserving their distinct public identities.
6. Validation confirms `catalog/generated/phase-b-arithmetic-support.json`
   is the authoritative arithmetic support matrix and enumerates every supported
   or intentionally unsupported path in scope exactly once.
7. Validation confirms `catalog/generated/phase-b-arithmetic-support.json`
   records the promoted result type, path family, and API mode for every
   supported arithmetic path in scope.
8. Dedicated tests cover every declared `ArithmeticError` and `ComputeError`
   variant directly.
9. Validation records absolute-temperature arithmetic paths as intentionally
   unsupported in the authoritative matrix.
10. Validation proves the free-function compute bridges are the authoritative
    boundary and that the matrix records their fixed result unit and result
    storage.

## Code Samples / Contracts

Representative semantics:

```rust
let lhs = Distance::cm(25.0);
let rhs = Distance::m(1.0);
let out = lhs + rhs;
assert_eq!(out.unit(), "cm");

let scaled = out * 2.0;
assert_eq!(scaled.unit(), "cm");
```

Promotion rule:

- the authoritative promotion rule is the subset of
  `catalog/generated/phase-b-arithmetic-support.json` whose `path_family` is
  `scalar_arithmetic`; that matrix must enumerate every supported
  `lhs_storage/operator/rhs_storage` combination exactly once
- `f64` dominates `f32`, signed integers, and unsigned integers
- `f32` dominates signed integers and unsigned integers when no `f64` operand is
  present
- signed integers dominate unsigned integers of equal or smaller width
- integer add/subtract/multiply paths are infallible only when the matrix
  selects a result storage that eliminates overflow for the documented operand
  pair; otherwise the path must be marked `checked`
- integer divide-by-scalar stays integer only when the matrix marks the path
  exact; otherwise callers must use a floating destination or an explicit
  checked path

Representative mixed-storage behavior:

```rust
let lhs = Distance::cm(25_i32);
let rhs = Distance::m(1.0_f64);
let out: Distance<f64> = lhs + rhs;

let scaled: Distance<f32> = Distance::cm(25_i32) * 2.5_f32;
let exact: Distance<i32> = Distance::cm(20_i32) / 2_i32;
let lossy = Distance::cm(1_i32).checked_div(2_i32);
assert!(lossy.is_err());
```

Representative promotion-matrix rows:

| lhs_storage | operator | rhs_storage | result_storage | path_family | api_mode | exact_division_policy | expected_failure |
|---|---|---|---|---|---|---|---|
| `i32` | `add` | `f64` | `f64` | `scalar_arithmetic` | `infallible` | not-applicable | none |
| `i32` | `mul` | `f32` | `f32` | `scalar_arithmetic` | `infallible` | not-applicable | none |
| `i32` | `add` | `i32` | `i32` | `scalar_arithmetic` | `checked` | not-applicable | `Overflow` when result exceeds `i32` |
| `i32` | `mul` | `i32` | `i32` | `scalar_arithmetic` | `checked` | not-applicable | `Overflow` when result exceeds `i32` |
| `i32` | `div` | `i32` | `i32` | `scalar_arithmetic` | `checked` | exact-only | `NonIntegralDivision` when remainder != 0 |

Representative compute bridge contract:

```rust
pub trait CheckedScalarArithmeticOps<Rhs = Self> {
    type Output;

    fn checked_add(self, rhs: Rhs) -> Result<Self::Output, ArithmeticError>;
    fn checked_sub(self, rhs: Rhs) -> Result<Self::Output, ArithmeticError>;
    fn checked_mul(self, rhs: Rhs) -> Result<Self::Output, ArithmeticError>;
    fn checked_div(self, rhs: Rhs) -> Result<Self::Output, ArithmeticError>;
}

pub enum ArithmeticError {
    NonIntegralDivision,
    Overflow,
    PrecisionLoss,
}

pub enum ComputeError {
    ZeroDuration,
    Overflow,
    PrecisionLoss,
}

pub fn velocity_from_distance_and_time(
    distance: Distance,
    duration: Time,
) -> Result<Velocity<f64>, ComputeError>;

pub fn acceleration_from_velocity_and_time(
    velocity: Velocity<f64>,
    duration: Time,
) -> Result<Acceleration<f64>, ComputeError>;
```

Authoritative compute-bridge rule:

- the free functions `velocity_from_distance_and_time` and
  `acceleration_from_velocity_and_time` are the normative compute-bridge
  surface for V1
- if later phases add convenience methods, those methods are derivative shims
  over the same free-function boundary rather than a second normative contract
- compute bridges return canonical compute units in fixed `f64` storage in V1

Result-identity rule:

- same-public-type arithmetic preserves the left-hand public quantity type and
  left-hand unit when the path is supported
- same-canonical-dimension cross-public-type arithmetic also preserves the
  left-hand public quantity type and left-hand unit when the authoritative
  matrix marks that exact path supported
- any cross-public-type pair not named supported in
  `catalog/generated/phase-b-arithmetic-support.json` is intentionally
  unsupported in V1
- unsupported type pairs and unsupported storage pairs are absent from the
  infallible and checked arithmetic traits rather than returning runtime
  `UnsupportedTypePair` or `UnsupportedStoragePair` variants

Representative cross-public-type example:

```rust
let lhs = Diopter::dpt(2.0);
let rhs = InverseDistance::per_m(0.5);
let out: Diopter = lhs + rhs;
assert_eq!(out.unit(), "dpt");
```

Representative compute-bridge matrix row:

| lhs_public_type | operator | rhs_public_type | result_public_type | result_storage | path_family | api_mode | expected_failure |
|---|---|---|---|---|---|---|---|
| `Distance` | `velocity_from_time` | `Time` | `Velocity` | `f64` | `compute_bridge` | `checked` | `ZeroDuration` when rhs == 0 |

Authoritative arithmetic-support artifact columns:

- `lhs_public_type`
- `lhs_unit`
- `lhs_storage`
- `operator`
- `rhs_public_type`
- `rhs_unit`
- `rhs_storage`
- `result_public_type`
- `result_unit_rule`
- `result_storage`
- `path_family`
- `api_mode`
- `exact_division_policy`
- `support_status`
- `expected_failure`

## Closure Gate

This sprint does not close until
`catalog/generated/phase-b-arithmetic-support.json` enumerates every supported
or intentionally unsupported arithmetic and compute-bridge path in scope
exactly once, including cross-public-type cases, their result-identity rule,
and the fixed result-storage rule for compute bridges.

V1 non-support boundary:

- this sprint does not promise reconstruction of the full legacy cross-dimension operator graph
- unsupported cross-dimension combinations must be documented as intentionally out of scope rather than silently omitted
