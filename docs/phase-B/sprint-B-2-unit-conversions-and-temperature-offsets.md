# Sprint B-2: Unit Conversions And Temperature Offsets

## Goal

Implement conversion logic for multiplicative units and MVP offset-temperature units.

## Status

`Not Started`

## Scope References

- REQ-UX-006
- REQ-UX-007
- REQ-UX-008
- REQ-UX-011
- REQ-UX-035
- REQ-UX-041
- REQ-UX-025
- REQ-UX-026
- REQ-UX-042
- REQ-UX-043
- REQ-UX-044
- REQ-UX-045
- ADR-UX-003
- ADR-UX-010
- ADR-UX-019
- ADR-UX-020
- ADR-UX-021

## Deliverables

1. Multiplicative conversions for the in-scope `base`, `geometry`, `mechanical`, and `electromagnetic` unit families
2. Celsius, Fahrenheit, and Kelvin conversion logic
3. Domain-reciprocal conversion logic for first-class reciprocal quantities, including `Diopter`
4. Reuse or adaptation of reference conversion-factor sources
5. Conversion-coverage completion for every item in
   [docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md)

## Dependencies

- Sprints A-2, A-3, B-1

## Unblocks

- Sprints B-3, C-1, E-1

## Acceptance Criteria

1. Multiplicative conversions are implemented for the in-scope unit families.
2. Celsius, Fahrenheit, and Kelvin conversion rules are explicit and correct.
3. Domain-reciprocal public units such as `Diopter` are explicitly supported.
4. Reference conversion-factor sources are either reused or mapped with no undocumented divergence.
5. The crate can represent the planned distance examples `mm`, `m`, and `ft`.
6. Potentially lossy storage conversions are routed through explicit fallible APIs.
7. The sprint cannot close while any in-scope type lacks a documented conversion status in the checklist for this sprint.

## Required Validation

1. Dedicated round-trip tests cover `mm -> m -> mm` and `ft -> m -> ft`.
2. Dedicated temperature tests cover negative values and offset-sensitive values such as freezing/boiling points.
3. Mixed conversion tests verify symbol/id handling does not confuse `C`/`degC`.
4. Dedicated tests cover a lossy integer-backed conversion failure path.
5. Dedicated tests cover `Distance::m(0.5) <-> Diopter::dpt(2.0)`.
6. Validation records conversion support status for every item in the
   authoritative inventory.

## Edge / Corner Conditions Requiring Dedicated Tests

1. Offset-temperature conversions where both scale and offset matter.
2. Negative temperature values.
3. Cross-system conversion between imperial and metric units.
4. Reciprocal-domain conversions between distance and diopter.

## Code Samples / Contracts

Representative API shape:

```rust
let distance = Distance::mm(1250.0);
let meters = distance.to::<m>();

let freezing = Temperature::degC(0.0);
let fahrenheit = freezing.to::<degF>();
assert_eq!(fahrenheit.value(), 32.0);

let focus = Distance::m(0.5).to::<dpt>();
assert_eq!(focus.value(), 2.0);

let exact = Distance::mm(1000_i32).try_to::<m_i32>()?;
let lossy = Distance::mm(1_i32).try_to::<m_i32>();
assert!(lossy.is_err());
```

## Conversion Checklist

The authoritative checklist for this sprint is
[docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md).
This sprint does not close until every item in that checklist has explicit
conversion support status implemented and tested.
