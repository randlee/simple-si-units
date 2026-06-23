# Sprint F-3: User Documentation And Examples

## Goal

Produce the final user-facing documentation and examples for the shipped
surfaces.

## Status

`Not Started`

## Scope References

- REQ-UX-012
- REQ-UX-013
- REQ-UX-014
- REQ-UX-015
- REQ-UX-016
- REQ-UX-019
- REQ-UX-032
- REQ-UX-033
- REQ-UX-040
- REQ-UX-042
- REQ-UX-043
- REQ-UX-044
- ADR-UX-005
- ADR-UX-014
- ADR-UX-020
- ADR-UX-021

## Deliverables

1. User-facing docs
2. Final user-facing cross-language examples
3. Final user-facing Python and C# examples
4. Cross-language JSON fixture and serialization parity signoff
5. Example/documentation coverage for every family in the authoritative in-scope inventory, including `Diopter`

## Dependencies

- Phase D
- Phase E
- Sprints F-1, F-2

## Unblocks

- Sprint F-4

## Acceptance Criteria

1. User docs cover installation, supported type surfaces, scalar usage, bulk usage, and serialization examples for shipped platforms.
2. Cross-language examples are consistent with canonical fixtures and the final API surface.
3. Rust, Python, and C# examples all agree on the canonical JSON wire shape, and any shipped binary-envelope examples agree on the canonical binary contract.
4. Examples and docs cover `base`, `geometry`, `mechanical`, `electromagnetic`, and `Diopter` surfaces explicitly enough that none of those families can be omitted by implication.
5. The docs distinguish the JSON DTO, binary-envelope, and C ABI surfaces rather than collapsing them into one undifferentiated serialization story.

## Required Validation

1. Example snippets are executable or test-backed.
2. Dedicated checks confirm example JSON matches canonical fixtures.
3. Dedicated review checks ensure docs do not promise unsupported surfaces.
4. Dedicated review checks confirm the example set covers every family in the authoritative inventory, including `Diopter`.
5. Dedicated review checks confirm that distinct public types sharing a canonical dimension, including `Diopter` and reciprocal-distance families, are documented without collapsing their identities.

## Example Coverage Checklist

The authoritative inventory for this sprint is
[docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md).
This sprint does not close until the documentation/example set explicitly
covers:

- [ ] `base`
- [ ] `geometry`
- [ ] `mechanical`
- [ ] `electromagnetic`
- [ ] `Diopter`
- [ ] canonical JSON examples for every shipped canonical JSON shape class
- [ ] binary-envelope examples for every shipped binary-envelope shape class
- [ ] C ABI examples for every shipped ABI shape class

## Non-Closure / Out Of Scope

- Publication dry runs
- Final release checklist closure
