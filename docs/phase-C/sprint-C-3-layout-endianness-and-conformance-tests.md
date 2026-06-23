# Sprint C-3: Layout, Endianness, And Conformance Tests

## Goal

Build the test suite for serialization and binary compatibility.

## Status

`Not Started`

## Scope References

- REQ-UX-013
- REQ-UX-017
- REQ-UX-018
- REQ-UX-031
- REQ-UX-032
- REQ-UX-033
- REQ-UX-037
- REQ-UX-038
- REQ-UX-039
- REQ-UX-040
- NFR-UX-003
- NFR-UX-004
- NFR-UX-005
- NFR-UX-013
- ADR-UX-005
- ADR-UX-012
- ADR-UX-017
- ADR-UX-018
- ADR-UX-011
- ADR-UX-014

## Deliverables

1. ABI layout tests
2. JSON fixture conformance tests
3. Binary schema conformance tests
4. Endianness tests
5. Golden serialization fixtures for canonical scalar and buffer cases
6. Determinism checks for catalog-derived type ids, unit ids, schema ids, and classification tags

## Dependencies

- Sprints C-1, C-2

## Unblocks

- Phase D
- Phase E
- Sprint F-2

## Acceptance Criteria

1. Layout, endianness, and contract-conformance tests exist for the Rust core.
2. JSON and binary contracts are both anchored by executable tests.
3. ABI layout assertions are explicitly separated from binary-envelope conformance assertions.
4. Golden fixtures are stable enough for downstream parity use.
5. The test plan covers the already-shipped ABI invariants as well as the new JSON and binary fixtures.

## Required Validation

1. Layout assertions cover the published scalar ABI structs, slice ABI structs, owned-buffer ABI structs, status-code width, and `u64` length fields.
2. Endianness tests cover at least one scalar payload and one buffer payload for the binary envelope contract.
3. Golden fixture tests fail on JSON-shape drift, binary-envelope drift, and catalog-derived identifier drift.
4. Dedicated ABI tests cover:
   - `null + zero` empty semantics
   - rejection of `null + non-zero`
   - owned-buffer destroy preconditions
   - documented overflow/status-code mappings
5. Dedicated binary-envelope tests cover:
   - catalog-derived schema ids
   - catalog-derived unit ids
   - schema-level unit metadata only
   - count/width/payload-size consistency
