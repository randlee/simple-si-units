# Architecture Index

## Purpose

This file is the root architecture index for `units-x`.

It defines the architecture documentation structure and the ADR id scheme,
while the crate-specific architectural decisions live in per-crate documents.

Detailed product and interop context remains in:

- [prd.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd.md)
- [prd-python.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-python.md)
- [prd-interop.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-interop.md)
- [project-plan.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/project-plan.md)

## Document Model

The architecture hierarchy is:

1. `docs/architecture.md`
2. one `architecture.md` per crate documentation folder

The convention is:

- root index: `docs/architecture.md`
- per-crate docs: `docs/crates/<crate-name>/architecture.md`

Crate architecture documents contain numbered ADRs. Design docs and planning
docs should reference those ADR ids rather than duplicating architectural
decisions in prose.

## Global Rules

### ADR-ROOT-001

Every shipped crate must have a corresponding architecture document under
`docs/crates/<crate-name>/architecture.md`.

### ADR-ROOT-002

Every per-crate architecture document must contain stable numbered ADR ids.

### ADR-ROOT-003

Planning docs, sprint docs, investigation docs, and design docs must cite the
relevant `ADR-*` ids when they depend on a specific architectural decision.

### ADR-ROOT-004

Architectural decisions that apply repo-wide may live in the root architecture
index, but crate-local decisions should live in the crate’s own
`architecture.md`.

### ADR-ROOT-005

Sprint documents are authoritative planning artifacts and must remain directly
consumable by implementation and QA without relying on downstream prompt
rewrites to narrow or reinterpret scope.

### ADR-ROOT-006

The repository’s top-level product roots are `reference/`, `crates/`,
`python/`, and `dotnet/`.

### ADR-ROOT-007

The Python deliverable baseline uses Rust bindings through PyO3, packaging
through `maturin`, and generated Pydantic models for canonical JSON types.

### ADR-ROOT-008

The `.NET` deliverable baseline uses Interoptopus-oriented binding generation,
blittable public structs where required by the ABI surface, user-facing C#
interfaces for the shipped quantity surface, and `System.Text.Json` parity
with canonical fixtures.

### ADR-ROOT-009

The repository execution baseline uses `just` as the primary task entrypoint
and `sc-lint` as a required lint layer for the shipped scope.

## ADR Id Scheme

Per-crate ADR ids use:

- `ADR-<CRATECODE>-NNN`

For the planned primary crate `units-x`, the crate code is `UX`.

Examples:

- `ADR-UX-001`
- `ADR-UX-002`

## Primary Crate

The primary crate for the planned deliverable is:

- `units-x`

This crate is the first and currently authoritative target for detailed ADR
numbering.

## Crate Architecture Index

| Crate | Status | Architecture Doc |
|---|---|---|
| `units-x` | Primary deliverable crate | [docs/crates/units-x/architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/architecture.md) |

Additional crates should be added here as they are introduced under `crates/`.

## Citation Rule

Planning and design references should use explicit ids, for example:

- `ADR-UX-001`
- `ADR-UX-003`

This is the intended source for:

- architecture traceability
- design review linkage
- QA architectural conformance review
- sprint/dependency justification
