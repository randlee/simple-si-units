# Sprint D-3: Go And C Consumer Examples

## Goal

Demonstrate that the same ABI works cleanly for Go and C.

## Status

`Not Started`

## Scope References

- REQ-UX-019
- REQ-UX-020
- REQ-UX-021
- NFR-UX-003
- NFR-UX-007
- ADR-UX-004
- ADR-UX-011

## Deliverables

1. C consumer smoke examples
2. Go consumer smoke examples
3. Smoke tests or example builds

## Dependencies

- Sprints C-3, D-1

## Unblocks

- Sprint F-3

## Parallelism

- Can run in parallel with Sprint D-2

## Acceptance Criteria

1. A C consumer example builds and uses the exported ABI successfully.
2. A Go consumer example builds and uses the exported ABI successfully.
3. The examples rely only on the documented C ABI contract, not Rust-specific assumptions.

## Required Validation

1. C compile smoke tests exist for at least one scalar and one slice case.
2. Go/cgo smoke tests exist for at least one scalar and one slice case.
3. Dedicated tests cover zero-length slice handling at the consumer boundary.
