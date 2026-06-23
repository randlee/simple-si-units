# Sprint F-2: Footprint, Layout, And Performance Validation

## Goal

Prove the minimum-footprint and ABI/layout claims made by the project.

## Status

`Not Started`

## Scope References

- NFR-UX-001
- NFR-UX-002
- NFR-UX-003
- NFR-UX-004
- NFR-UX-005
- ADR-UX-014
- ADR-UX-011

## Deliverables

1. Size assertions for scalar and bulk wrappers
2. Final repo-wide ABI layout regression assertions
3. JSON and binary serialization overhead checks
4. Focused performance or copy-behavior checks for Rust bulk encode/decode, C ABI slice pass-through, Python memoryview ingestion, and C# `Span<T>` consumption

## Dependencies

- Sprints B-4, C-3, D-1

## Unblocks

- Sprint F-3

## Parallelism

- Can run in parallel with Sprint F-1

## Acceptance Criteria

1. Scalar and bulk wrapper footprint claims are backed by executable assertions.
2. Final ABI layout regressions are guarded by tests.
3. Serialization and copy-overhead checks exist for Rust bulk encode/decode, JSON envelope generation, C ABI slice pass-through, Python memoryview ingestion, and C# `Span<T>` consumption.

## Required Validation

1. `size_of` assertions cover every unique wrapper/storage layout class used by
   the authoritative in-scope type inventory, and validation maps each public
   type to one of those checked layout classes.
2. Dedicated layout regression tests cover exported ABI structs.
3. Dedicated checks cover zero-copy or copy-count expectations where the plan makes that claim.
4. Dedicated checks cover JSON and binary-envelope overhead expectations wherever the architecture makes compactness claims.
