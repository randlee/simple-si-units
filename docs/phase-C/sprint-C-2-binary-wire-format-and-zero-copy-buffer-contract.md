# Sprint C-2: Binary Wire Format And Zero-Copy Buffer Contract

## Goal

Define the binary interchange format and zero-copy expectations for bulk data.

## Status

`Not Started`

## Scope References

- REQ-UX-013
- REQ-UX-018
- REQ-UX-021
- REQ-UX-022
- REQ-UX-039
- REQ-UX-040
- NFR-UX-003
- NFR-UX-004
- NFR-UX-013
- ADR-UX-005
- ADR-UX-017
- ADR-UX-011
- ADR-UX-012
- ADR-UX-018

## Deliverables

1. Binary metadata contract
2. Raw payload contract
3. Rules for endianness and numeric widths
4. Rules for schema-level versus per-element unit metadata
5. Binary-safe unit-id namespace and wire-format versioning policy

## Dependencies

- Sprints A-2, A-3, B-4

## Unblocks

- Sprints D-1, D-2, D-3, E-2, F-2

## Acceptance Criteria

1. The binary metadata contract is explicit for little-endian version fields, type id, unit id, count, width, and encoding.
2. The raw payload contract is explicit and unambiguous.
3. Endianness and numeric-width rules are fixed and documented.
4. ABI and binary-contract expectations are documented as related but separate contracts.

## Required Validation

1. Dedicated conformance tests cover little-endian encoded payloads.
2. Dedicated tests reject unknown schema/version or binary-safe unit ids.
3. Dedicated tests cover `count`/payload-size mismatch failures.

## Code Samples / Contracts

Representative binary envelope fields:

```text
u16 version_le
u16 type_id_le
u32 unit_id_le
u8 element_width
u8 flags
u16 reserved
u64 count_le
payload[count * element_width] in little-endian element order
```
