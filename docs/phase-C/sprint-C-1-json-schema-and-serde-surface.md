# Sprint C-1: JSON Schema And Serde Surface

## Goal

Create the explicit JSON representation and serde integration for scalar and bulk quantities.

## Status

`Not Started`

## Deliverables

1. Scalar JSON schema
2. Fixed small-buffer JSON array schema
3. Large/arbitrary-buffer encoded JSON schema
4. Rust serde integration
5. Round-trip tests
6. Canonical fixture set for cross-language parity
7. Catalog-driven JSON schema generation strategy
8. Machine-readable classification of which public types use inline arrays versus encoded payload envelopes

## Dependencies

- Sprints A-2, A-5, B-2, B-3

## Unblocks

- Sprints E-1, E-3, F-1

## Exit Criteria

1. JSON includes explicit canonical type ids and human-readable unit metadata where needed.
2. JSON is independent from internal Rust field naming.
3. Canonical fixtures exist for Python and C# parity testing.
4. Public type classification into array-form versus encoded-buffer JSON is explicit and generated from source-of-truth metadata.
