# Sprint C-2: Binary Wire Format And Zero-Copy Buffer Contract

## Goal

Define the binary interchange format and the buffer-envelope borrowing rules for
bulk data without conflating that contract with the Rust ABI surface.

## Status

`Not Started`

## Scope References

- REQ-UX-013
- REQ-UX-018
- REQ-UX-021
- REQ-UX-022
- REQ-UX-037
- REQ-UX-038
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
5. Binary-safe schema-id and unit-id namespace plus wire-format versioning policy
6. Explicit statement of what "zero-copy" means for:
   - owned byte envelopes
   - borrowed byte envelopes
   - typed borrowed Rust bulk views
7. Separation note between binary envelopes and the ABI slice/owned-buffer contract

## Dependencies

- Sprints A-2, A-3, B-4, B-5

## Unblocks

- Sprints D-1, D-2, D-3, E-2, F-2

## Acceptance Criteria

1. The binary metadata contract is explicit for little-endian version fields, catalog-derived schema id, catalog-derived unit id, count, element width, and flags.
2. The raw payload contract is explicit and unambiguous.
3. Endianness and numeric-width rules are fixed and documented.
4. ABI and binary-contract expectations are documented as related but separate contracts.
5. The binary contract uses one schema-level unit id per envelope and explicitly rejects heterogeneous per-element unit metadata in V1.
6. The plan defines when byte-level zero-copy is valid and when consumers must copy or transcode.

## Required Validation

1. Dedicated conformance tests cover little-endian encoded payloads.
2. Dedicated tests reject unknown schema/version or binary-safe unit ids.
3. Dedicated tests cover `count`/payload-size mismatch failures.
4. Dedicated tests cover schema-level unit metadata only and reject any attempted per-element unit payload decoration in V1.
5. Dedicated tests distinguish binary-envelope validation failures from ABI pointer/length validation failures.

## Code Samples / Contracts

Representative binary envelope fields:

```text
u16 envelope_version_le
u16 flags_le
u32 reserved_le
u64 count_le
u32 element_width_le
u32 schema_id_len_le
u32 unit_id_len_le
utf8[schema_id_len] schema_id
utf8[unit_id_len] unit_id
payload[count * element_width] in little-endian element order
```

Authoritative binary-boundary rule:

- `schema_id` is the catalog-derived binary schema id such as
  `units-x.distance.v1`
- `unit_id` is the catalog-derived binary unit id such as `distance.mm`
- V1 binary envelopes are homogeneous and carry one unit id at the
  envelope/schema level
- this sprint defines binary byte-envelope rules, not the C ABI pointer/length
  contract from `ffi_contract`
- "zero-copy" in V1 means:
  - byte envelopes may be borrowed as raw bytes when version, endianness,
    width, and alignment expectations already match the consumer
  - typed Rust `QuantityBufferView<'a, Unit, T>` remains a separate public API
    and is not itself the canonical binary envelope
