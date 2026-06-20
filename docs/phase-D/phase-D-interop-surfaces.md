# Phase D: Interop Surfaces

## Goal

Create the stable C ABI and the first non-Python interop surfaces for C#, Go, C, and Rust consumers, including the `.NET` package path under `dotnet/`.

## Status

`Not Started`

## Phase Dependencies

- [Phase B](../phase-B/phase-B-core-quantity-model.md)
- [Phase C](../phase-C/phase-C-serialization-and-binary-contract.md)

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint D-1](sprint-D-1-stable-c-abi-types-and-exported-functions.md) | Stable C ABI types and exported functions | Sprints B-3, B-4, C-2 | None | `Not Started` |
| [Sprint D-2](sprint-D-2-csharp-interoptopus-bindings-and-span-friendly-surface.md) | C# and Interoptopus bindings plus span-friendly surface | Sprints D-1, A-3 | Sprint D-3 | `Not Started` |
| [Sprint D-3](sprint-D-3-go-and-c-consumer-examples.md) | Go and C consumer examples and smoke tests | Sprint D-1 | Sprint D-2 | `Not Started` |

## Phase Completion Criteria

Phase D is complete when:

1. Stable exported ABI types exist.
2. C# has a clean binding path.
3. Go and C consumption are demonstrated.
4. The `.NET` wrapper/package path is structurally ready for NuGet publication.
