# Sprint C-1: JSON Schema And Serde Surface

## Goal

Create the explicit JSON representation and serde integration for scalar and bulk quantities.

## Status

`Not Started`

## Deliverables

1. Scalar JSON schema
2. Array JSON schema
3. Rust serde integration
4. Round-trip tests
5. Canonical fixture set for cross-language parity
6. Catalog-driven JSON schema generation strategy

## Dependencies

- Sprints B-2, B-3

## Unblocks

- Sprints E-1, E-3, F-1

## Exit Criteria

1. JSON includes explicit dimension, unit, and storage metadata where needed.
2. JSON is independent from internal Rust field naming.
3. Canonical fixtures exist for Python and C# parity testing.
