# Requirements Index

## Purpose

This file is the root requirements index for `units-x`.

It does not attempt to duplicate every crate-level requirement inline. Instead,
it establishes:

- repo-wide requirement rules
- the crate documentation structure
- the requirement id scheme
- the authoritative per-crate requirements documents to cite

Detailed product background remains in:

- [prd.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd.md)
- [prd-python.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-python.md)
- [prd-interop.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-interop.md)

If a PRD conflicts with this index, align this file and the affected crate docs
to the PRD or explicitly revise the PRD.

## Document Model

The requirements hierarchy is:

1. `docs/requirements.md`
2. one `requirements.md` per crate documentation folder

The convention is:

- root index: `docs/requirements.md`
- per-crate docs: `docs/crates/<crate-name>/requirements.md`

Design documents, planning documents, and sprint documents must cite numbered
requirement ids from the per-crate docs instead of restating requirements as
free-form prose.

## Global Rules

These root rules apply across all crates.

### REQ-ROOT-001

Every shipped crate must have a corresponding requirements document under
`docs/crates/<crate-name>/requirements.md`.

### REQ-ROOT-002

Every per-crate requirements document must contain stable numbered requirement
ids.

### REQ-ROOT-003

Functional requirements in per-crate docs must use the `REQ-` prefix.

### REQ-ROOT-004

Non-functional requirements in per-crate docs must use the `NFR-` prefix.

### REQ-ROOT-005

Requirement ids must be stable once published in planning or design documents.
If wording changes, preserve the id unless the requirement is materially split
or replaced.

### REQ-ROOT-006

Design docs, investigation docs, planning docs, and sprint docs must reference
the applicable `REQ-*` and `NFR-*` ids rather than inventing parallel unnamed
requirements.

### REQ-ROOT-007

Sprint planning documents must follow
`.claude/skills/plan-hardening/sprint-planning-guidelines.md`.

### REQ-ROOT-008

Each sprint document must contain one authoritative list for:

- deliverables
- acceptance criteria
- required validation

### REQ-ROOT-009

If QA cannot review directly from a sprint document, that sprint document is
not considered hardened.

### REQ-ROOT-010

All shipped Rust, Python, and `.NET` artifacts must derive their publish
version from one machine-readable repository source of truth.

### REQ-ROOT-011

Normal repository validation and CI must fail when published artifact metadata
drifts from the shared version source of truth.

### REQ-ROOT-012

`docs/project-plan.md` and each phase-overview document under `docs/phase-*/`
are planning documents for the purposes of `REQ-ROOT-006` and must contain
explicit scope references.

### REQ-ROOT-013

The repository must maintain first-class top-level roots for `reference/`,
`crates/`, `python/`, and `dotnet/`.

### REQ-ROOT-014

The Python deliverable must be publish-ready for PyPI/pip and participate in
the shared version-lock model.

### REQ-ROOT-015

The `.NET` deliverable must be publish-ready for NuGet and participate in the
shared version-lock model.

### REQ-ROOT-016

The Python binding and packaging baseline must use PyO3 and `maturin`.

### REQ-ROOT-017

Generated Pydantic models must exist for every public canonical JSON type and
must preserve the canonical wire shape.

### REQ-ROOT-018

The `.NET` deliverable must provide ABI-compatible public structs for the
shipped interop surface, `Span<T>`-friendly consumption for the shipped bulk
surface, and
`System.Text.Json` support for the canonical JSON wire shape.

### REQ-ROOT-021

The `.NET` deliverable must provide user-facing C# interfaces over the shipped
quantity surface so application code is not forced to depend directly on raw
ABI structs alone.

### REQ-ROOT-019

The `.NET` deliverable must synchronize package metadata through
`Directory.Build.props` or an equivalent repo-centralized mechanism wired to
the shared version source.

### REQ-ROOT-020

The repository execution baseline must provide `just build`, `just test`, and
subsystem-oriented `just test ...` entrypoints, and must run the required
`sc-lint` checks for the shipped scope.

## Id Scheme

Per-crate requirement ids use:

- functional: `REQ-<CRATECODE>-NNN`
- non-functional: `NFR-<CRATECODE>-NNN`

For the planned primary crate `units-x`, the crate code is `UX`.

Examples:

- `REQ-UX-001`
- `REQ-UX-002`
- `NFR-UX-001`

## Primary Crate

The primary crate for the planned deliverable is:

- `units-x`

This crate is the first and currently authoritative target for detailed
requirement numbering.

## Crate Requirements Index

| Crate | Status | Requirements Doc |
|---|---|---|
| `units-x` | Primary deliverable crate | [docs/crates/units-x/requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/requirements.md) |

Additional crates should be added here as they are introduced under `crates/`.

## Citation Rule

Planning and design references should use explicit ids, for example:

- `REQ-UX-003`
- `NFR-UX-002`

This is the intended source for:

- sprint acceptance criteria linkage
- design justification
- QA traceability
- change impact review
