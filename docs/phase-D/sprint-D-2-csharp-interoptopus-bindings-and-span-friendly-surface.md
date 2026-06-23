# Sprint D-2: C# Interoptopus Bindings And Span-Friendly Surface

## Goal

Generate or author a clean C# binding surface on top of the C ABI, including
blittable public structs and `Span<T>`-friendly APIs.

## Status

`Not Started`

## Scope References

- REQ-ROOT-018
- REQ-ROOT-021
- REQ-UX-019
- REQ-UX-020
- REQ-UX-021
- REQ-UX-022
- REQ-UX-037
- REQ-UX-038
- REQ-UX-040
- NFR-UX-004
- NFR-UX-003
- NFR-UX-007
- ADR-ROOT-008
- ADR-UX-004
- ADR-UX-011
- ADR-UX-017

## Deliverables

1. Low-level generated binding layer
2. Public blittable C# quantity structs for every shipped ABI row that is surfaced to C#
3. User-facing C# interfaces for scalar and bulk quantity contracts
4. `Span<T>` and `ReadOnlySpan<T>` helpers over ABI-compatible structs
5. Ergonomic conversion and formatting helpers over the ABI-compatible structs
6. Inventory mapping exported ABI rows to generated and public C# rows

## Dependencies

- Sprints A-3, D-1

## Unblocks

- Sprint D-4

## Parallelism

- Can run in parallel with Sprint D-3

## Acceptance Criteria

1. The low-level Interoptopus-generated binding layer exists and is reproducible.
2. Public C# quantity structs are blittable and ABI-compatible for every shipped ABI row surfaced to C#.
3. User-facing C# interfaces exist for the shipped scalar and bulk quantity surface without omitting any planned C#-visible type family.
4. `Span<T>` and `ReadOnlySpan<T>` helpers work over the public structs without extra element wrapping.
5. The ergonomic helpers and interfaces do not hide or violate the documented ABI ownership and lifetime rules.
6. The sprint closure inventory shows no shipped ABI row omitted from the intended C# surface.

## Required Validation

1. Dedicated tests confirm blittable layout assumptions for public C# structs.
2. Dedicated tests cover `Span<T>` consumption of scalar arrays/buffers.
3. Dedicated tests confirm shipped C# interfaces can be implemented by or projected from the public structs/wrappers used by the package.
4. Dedicated checks confirm the generated binding layer can be regenerated without manual edits.
5. Validation records which shipped ABI rows intentionally remain low-level-only and confirms that no planned public C# row is absent.

## Code Samples / Contracts

```csharp
public interface IDistanceMF64
{
    double ValueM { get; }
}

public partial struct DistanceMF64
{
    public double value_m;
}

public readonly ref struct DistanceMF64SpanView
{
    public ReadOnlySpan<DistanceMF64> Values { get; }
}

ReadOnlySpan<DistanceMF64> values = ...;
```
