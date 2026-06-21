# Phase C: Serialization And Binary Contract

## Goal

Define and implement explicit JSON and binary serialization paths with strong layout guarantees.

## Status

`Not Started`

## Scope References

- REQ-UX-012
- REQ-UX-013
- REQ-UX-014
- REQ-UX-015
- REQ-UX-016
- REQ-UX-017
- REQ-UX-018
- REQ-UX-021
- REQ-UX-032
- REQ-UX-033
- REQ-UX-036
- NFR-UX-003
- NFR-UX-004
- NFR-UX-005
- ADR-UX-005
- ADR-UX-010
- ADR-UX-011
- ADR-UX-012
- ADR-UX-014

## Phase Dependencies

- [Phase B](../phase-B/phase-B-core-quantity-model.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint C-1](sprint-C-1-json-schema-and-serde-surface.md) | JSON schema and serde surface | Sprints A-2, B-2, B-3 | None | `Not Started` |
| [Sprint C-2](sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md) | Binary wire format and zero-copy buffer contract | Sprints A-2, A-3, B-4 | None | `Not Started` |
| [Sprint C-3](sprint-C-3-layout-endianness-and-conformance-tests.md) | Layout, endianness, and wire conformance tests | Sprints C-1, C-2 | None | `Not Started` |

## Phase Completion Criteria

Phase C is complete when:

1. JSON serialization is explicit, stable, and canonical in the Rust core with shared fixtures for downstream language bindings.
2. Binary serialization is explicit and documented as a contract separate from the in-memory ABI.
3. Layout and compatibility tests exist.
