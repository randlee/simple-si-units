# Sprint D-3: Go And C Consumer Examples

## Goal

Prove that the same documented ABI works cleanly for Go and C without
Rust-specific assumptions.

## Status

`Not Started`

## Scope References

- REQ-UX-022
- REQ-UX-019
- REQ-UX-020
- REQ-UX-021
- REQ-UX-037
- REQ-UX-038
- NFR-UX-003
- NFR-UX-004
- NFR-UX-007
- ADR-UX-004
- ADR-UX-011

## Deliverables

1. C consumer conformance examples
2. Go consumer conformance examples
3. Example builds or test-backed consumer checks
4. ABI shape-class coverage matrix for the Go and C examples

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
4. The examples collectively cover every shipped ABI shape class that Phase D exposes to non-.NET consumers.

## Required Validation

1. C compile smoke tests exist for every shipped ABI shape class surfaced in the C example set.
2. Go/cgo smoke tests exist for every shipped ABI shape class surfaced in the Go example set.
3. Dedicated tests cover zero-length slice handling at the consumer boundary.
4. Dedicated tests or review checks cover status handling and owned-buffer destruction wherever those contracts are shipped.
