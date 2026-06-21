# Sprint C-1: JSON Schema And Serde Surface

## Goal

Create the explicit JSON representation and serde integration for scalar and bulk quantities.

## Status

`Not Started`

## Scope References

- REQ-UX-012
- REQ-UX-014
- REQ-UX-015
- REQ-UX-016
- REQ-UX-017
- REQ-UX-032
- REQ-UX-033
- REQ-UX-036
- ADR-UX-005
- ADR-UX-010
- ADR-UX-012
- ADR-UX-014

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

- Sprints D-4, E-1, E-3, F-1

## Acceptance Criteria

1. The scalar JSON shape is explicit, stable, and documented.
2. The fixed small-buffer JSON array shape is explicit, stable, and documented.
3. The large/arbitrary-buffer JSON envelope shape is explicit, stable, and documented.
4. Public type classification into array-form versus encoded-buffer JSON is source-of-truth metadata, not serializer guesswork.
5. Canonical fixtures exist for downstream parity consumers.

## Required Validation

1. Round-trip serde tests cover scalar, fixed-array, and encoded-buffer forms.
2. Dedicated tests reject mismatched `type` and `unit` combinations where the contract requires consistency.
3. Dedicated tests cover `C`/`F` wire symbols for temperature.
4. Dedicated tests cover the boundary between inline-array and encoded-buffer classification.

## Code Samples / Contracts

Representative scalar JSON:

```json
{
  "type": "temperature_f32",
  "unit": "C",
  "value": 25.0
}
```

Representative fixed-buffer JSON:

```json
{
  "type": "distance3_f32",
  "unit": "cm",
  "values": [12.0, 15.0, 18.0]
}
```

Representative encoded-buffer JSON:

```json
{
  "type": "temperature_buffer_f32",
  "unit": "C",
  "encoding": "base64-le-f32",
  "count": 16384,
  "data": "AAAgQQAAKEEAACRBAAAYQQ=="
}
```
