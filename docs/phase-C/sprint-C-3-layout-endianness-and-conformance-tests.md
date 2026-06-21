# Sprint C-3: Layout, Endianness, And Conformance Tests

## Goal

Build the test suite for serialization and binary compatibility.

## Status

`Not Started`

## Scope References

- REQ-UX-031
- REQ-UX-032
- NFR-UX-003
- NFR-UX-004
- NFR-UX-005
- NFR-UX-013
- ADR-UX-005
- ADR-UX-011
- ADR-UX-014

## Deliverables

1. Layout tests
2. Endianness tests
3. Binary schema conformance tests
4. Golden serialization fixtures for canonical scalar and buffer cases

## Dependencies

- Sprints C-1, C-2

## Unblocks

- Phase D
- Phase E
- Sprint F-2

## Acceptance Criteria

1. Layout, endianness, and contract-conformance tests exist for the Rust core.
2. JSON and binary contracts are both anchored by executable tests.
3. Golden fixtures are stable enough for downstream parity use.

## Required Validation

1. Layout assertions cover scalar ABI structs and slice ABI structs where available.
2. Endianness tests cover at least one scalar and one buffer case.
3. Golden fixture tests fail on wire-shape drift.
