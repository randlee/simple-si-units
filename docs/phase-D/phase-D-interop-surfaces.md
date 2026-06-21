# Phase D: Interop Surfaces

## Goal

Create the stable C ABI and the first non-Python interop surfaces for C#, Go, C, and Rust consumers, including the `.NET` package path under `dotnet/`.

## Status

`Not Started`

## Scope References

- REQ-ROOT-015
- REQ-ROOT-018
- REQ-ROOT-021
- REQ-ROOT-019
- REQ-UX-019
- REQ-UX-020
- REQ-UX-021
- REQ-UX-022
- REQ-UX-033
- NFR-UX-003
- NFR-UX-004
- NFR-UX-007
- ADR-ROOT-008
- ADR-UX-004
- ADR-UX-005
- ADR-UX-011
- ADR-UX-014

## Phase Dependencies

- [Phase B](../phase-B/phase-B-core-quantity-model.md)
- [Phase C](../phase-C/phase-C-serialization-and-binary-contract.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint D-1](sprint-D-1-stable-c-abi-types-and-exported-functions.md) | Stable C ABI types and exported functions | Sprints A-3, B-2, B-3, B-4, C-2, C-3 | None | `Not Started` |
| [Sprint D-2](sprint-D-2-csharp-interoptopus-bindings-and-span-friendly-surface.md) | C# and Interoptopus bindings plus span-friendly surface | Sprints A-3, D-1 | Sprint D-3 | `Not Started` |
| [Sprint D-3](sprint-D-3-go-and-c-consumer-examples.md) | Go and C consumer smoke examples and integration checks | Sprints C-3, D-1 | Sprint D-2 | `Not Started` |
| [Sprint D-4](sprint-D-4-csharp-json-and-packaging.md) | C# canonical JSON surface and `.NET` packaging readiness | Sprints C-1, D-2 | Sprint D-3 | `Not Started` |

## Phase Completion Criteria

Phase D is complete when:

1. Stable exported ABI types exist.
2. C# has a clean binding path, user-facing interface layer, and canonical JSON support.
3. Go and C consumption are demonstrated.
4. The `.NET` wrapper/package path is structurally ready for NuGet publication.
