# Sprint A-3: ABI And Unit Naming Contract

## Goal

Lock the fundamental naming, layout, and ABI rules for the project.

## Status

`Not Started`

## Deliverables

1. Concrete rule for ABI-facing struct naming
2. Concrete rule for type-level unit marker naming and symbol casing
3. Concrete rule for slice layout and length width
4. Concrete rule for FFI-safe ownership boundaries
5. Concrete rule distinguishing in-memory ABI layout from binary wire format

## Why

This project depends on stable, cross-language behavior. Naming and layout rules must be frozen before code generation and wrapper generation.

## Dependencies

- Sprint A-1

## Unblocks

- Sprint B-1
- Sprint C-2
- Sprint D-1
- Sprint D-2
- Sprint D-3

## Parallelism

- Can run in parallel with Sprint A-4 after Sprint A-1

## Exit Criteria

1. Public ABI naming and layout rules are documented, including a fixed-width slice length choice.
2. Unit marker casing rules cover cases such as `mm`, `Mm`, `degC`, and `degF`.
3. Wire/display unit symbols are documented separately from safe code identifiers where they differ, such as `C` versus `degC`.
