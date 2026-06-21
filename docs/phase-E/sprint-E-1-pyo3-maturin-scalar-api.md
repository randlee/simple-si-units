# Sprint E-1: PyO3/Maturin Scalar API

## Goal

Implement the high-level Python scalar quantity API.

## Status

`Not Started`

## Scope References

- REQ-ROOT-016
- REQ-UX-008
- REQ-UX-012
- REQ-UX-014
- REQ-UX-023
- REQ-UX-024
- REQ-UX-025
- REQ-UX-026
- NFR-UX-007
- ADR-UX-004
- ADR-UX-005
- ADR-UX-010

## Deliverables

1. PyO3 scalar classes or functions
2. Unit-specific constructors and accessors
3. Temperature support including Celsius/Fahrenheit
4. Velocity and acceleration scalar surface for the V1 set
5. Packaging path using `maturin`
6. `abi3` viability decision and supported Python-floor policy
7. Initial package structure under `python/`

## Dependencies

- Sprints B-2, B-3, C-1, C-3

## Unblocks

- Sprint E-3

## Acceptance Criteria

1. The Python scalar API exposes explicit unit-specific constructors and accessors.
2. Temperature scalar support includes the planned Celsius/Fahrenheit behavior.
3. Velocity and acceleration scalar APIs exist for the V1 derived set.
4. Packaging works through the repo `maturin` workflow.
5. The `abi3` strategy is explicitly implemented or explicitly rejected with rationale.

## Required Validation

1. Dedicated Python tests cover scalar construction, conversion, and display.
2. Dedicated tests cover temperature symbol behavior using `C`/`F` at the wire level.
3. Wheel/package build tests verify the version comes from the shared project source.

## Code Samples / Contracts

```python
d = Distance.mm(1250)
t = Time.s(2.0)
v = d.velocity_over(t)
assert abs(v.mps() - 0.625) < 1e-12
```
