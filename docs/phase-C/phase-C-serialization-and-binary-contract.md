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
- REQ-UX-022
- REQ-UX-021
- REQ-UX-037
- REQ-UX-038
- REQ-UX-039
- REQ-UX-040
- REQ-UX-032
- REQ-UX-033
- REQ-UX-036
- NFR-UX-003
- NFR-UX-004
- NFR-UX-005
- NFR-UX-013
- ADR-UX-005
- ADR-UX-010
- ADR-UX-011
- ADR-UX-012
- ADR-UX-017
- ADR-UX-014
- ADR-UX-018

## Phase Dependencies

- [Phase B](../phase-B/phase-B-core-quantity-model.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint C-1](sprint-C-1-json-schema-and-serde-surface.md) | JSON schema, serde surface, and canonical JSON fixtures | Sprints A-2, A-5, B-2, B-3, B-4 | None | `Not Started` |
| [Sprint C-2](sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md) | Binary wire format and buffer-envelope contract | Sprints A-2, A-3, B-4, B-5 | None | `Not Started` |
| [Sprint C-3](sprint-C-3-layout-endianness-and-conformance-tests.md) | Layout, endianness, and wire conformance tests | Sprints C-1, C-2 | None | `Not Started` |

## Phase Completion Criteria

Phase C is complete when:

1. JSON serialization is explicit, stable, and canonical in the Rust core with shared fixtures for downstream language bindings.
2. Binary serialization is explicit and documented as a contract separate from the in-memory ABI.
3. Catalog-derived JSON type ids, binary schema ids, binary unit ids, and JSON/buffer classification metadata remain the only naming and classification authority.
4. The plan explicitly distinguishes:
   - JSON DTO contracts
   - binary envelope contracts
   - ABI layout and ownership contracts
5. Layout, determinism, and compatibility tests exist for each of those layers.
