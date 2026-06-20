# Sprint D-2: C# Interoptopus Bindings And Span-Friendly Surface

## Goal

Generate or author a clean C# surface on top of the C ABI, including blittable public structs and `Span<T>`-friendly APIs.

## Status

`Not Started`

## Deliverables

1. Low-level generated binding layer
2. Public blittable C# quantity structs
3. `Span<T>` and `ReadOnlySpan<T>` helpers over ABI-compatible structs
4. Ergonomic conversion and formatting helpers
5. `System.Text.Json`-compatible JSON surface matching canonical fixtures
6. `.NET` packaging metadata under `dotnet/`, including `Directory.Build.props` version integration

## Dependencies

- Sprints A-3, D-1

## Unblocks

- Sprint F-3

## Parallelism

- Can run in parallel with Sprint D-3

## Exit Criteria

1. Public C# quantity structs are ABI-compatible and usable in spans.
2. The C# consumer experience is clean for single values and bulk values.
3. C# JSON serialization matches the canonical wire shape directly.
4. The C# package metadata is wired to the shared version source.
