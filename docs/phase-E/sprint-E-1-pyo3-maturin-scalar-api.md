# Sprint E-1: PyO3/Maturin Scalar API

## Goal

Implement the high-level Python scalar quantity API.

## Status

`Not Started`

## Deliverables

1. PyO3 scalar classes or functions
2. Unit-specific constructors and accessors
3. Temperature support including Celsius/Fahrenheit
4. Velocity and acceleration scalar surface for the V1 set
5. Packaging baseline using `maturin`
6. `abi3` viability decision and supported Python-floor policy
7. Initial package structure under `python/`

## Dependencies

- Sprints B-2, B-3, C-1, C-3

## Unblocks

- Sprint E-3

## Exit Criteria

1. Python scalars are ergonomic and explicit.
2. Wheel packaging works in the baseline build.
3. The Python package reads its version from the shared project version source.
4. The `abi3` strategy is either implemented or explicitly rejected with a documented fallback.
