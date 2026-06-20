# Phase C: Serialization And Binary Contract

## Goal

Define and implement explicit JSON and binary serialization paths with strong layout guarantees.

## Status

`Not Started`

## Phase Dependencies

- [Phase B](../phase-B/phase-B-core-quantity-model.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint C-1](sprint-C-1-json-schema-and-serde-surface.md) | JSON schema and serde surface | Sprints B-2, B-3 | None | `Not Started` |
| [Sprint C-2](sprint-C-2-binary-wire-format-and-zero-copy-buffer-contract.md) | Binary wire format and zero-copy buffer contract | Sprints B-4, A-3 | None | `Not Started` |
| [Sprint C-3](sprint-C-3-layout-endianness-and-conformance-tests.md) | Layout, endianness, and wire conformance tests | Sprints C-1, C-2 | None | `Not Started` |

## Phase Completion Criteria

Phase C is complete when:

1. JSON serialization is explicit, stable, and canonical across language bindings.
2. Binary serialization is explicit and documented.
3. Layout and compatibility tests exist.
