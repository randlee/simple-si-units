# Sprint D-4: C# JSON And Packaging

## Goal

Complete the C# canonical JSON surface and `.NET` package metadata on top of
the binding layer.

## Status

`Not Started`

## Scope References

- REQ-ROOT-015
- REQ-ROOT-018
- REQ-ROOT-019
- REQ-UX-012
- REQ-UX-014
- REQ-UX-015
- REQ-UX-016
- REQ-UX-032
- REQ-UX-033
- REQ-UX-036
- REQ-UX-040
- NFR-UX-007
- NFR-UX-011
- NFR-UX-013
- ADR-ROOT-008
- ADR-UX-005
- ADR-UX-014

## Deliverables

1. Generated or adjacent `System.Text.Json` DTO or converter surface matching canonical fixtures
2. C# canonical JSON parity tests
3. `.NET` package metadata under `dotnet/`, including `Directory.Build.props` version integration
4. NuGet publication metadata and local packaging path documentation
5. Authoritative fixture-to-C# JSON inventory for every shipped canonical JSON shape

## Dependencies

- Sprints C-1, D-2

## Unblocks

- Sprint F-3
- Sprint F-4

## Parallelism

- Can run in parallel with Sprint D-3 after Sprint D-2

## Acceptance Criteria

1. The C# JSON surface matches canonical fixtures without semantic drift.
2. The mapping from ABI-compatible structs to JSON-facing DTO and converter surfaces is generated or trivial and documented for every shipped canonical JSON shape.
3. `.NET` package metadata is wired to the shared version source.
4. NuGet-oriented packaging metadata is explicit enough for release-readiness work to proceed without reopening design questions.
5. The sprint closure inventory shows no shipped canonical JSON type omitted from the C# surface.

## Required Validation

1. `System.Text.Json` output matches canonical fixtures for every shipped canonical JSON shape class, including scalar, small-buffer, and encoded-buffer forms where shipped.
2. Dedicated tests cover `C` and `F` unit-symbol handling in the C# JSON layer.
3. Version synchronization reaches `Directory.Build.props`.
4. A local `dotnet pack` path is documented and reproducible from normal repo tooling.

## Code Samples / Contracts

```csharp
public sealed record TemperatureF32Json(
    string type,
    string unit,
    float value
);
```
