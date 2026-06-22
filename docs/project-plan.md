# Project Plan

## Status Legend

- `Not Started`
- `In Progress`
- `Blocked`
- `Done`

## Overview

This plan covers the new deliverable crate for unit-preserving quantities with:

- minimum storage footprint
- stable C ABI
- JSON and binary serialization
- C#/Go/C/Rust interop
- Python integration via PyO3/maturin
- master-catalog-driven code generation and test generation

The authoritative MVP public type surface is the catalog-derived summary at
`catalog/generated/units-catalog-summary.json`, covering the `base`,
`geometry`, `mechanical`, and `electromagnetic` families plus `Diopter`.
[docs/crates/units-x/in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md)
is a derived reference checklist for human review and must not become a second
planning or validation authority.

The existing `simple-si-units` crates remain reference and validation oracles under `reference/`, not the primary deliverable.

## Scope References

- REQ-ROOT-006
- REQ-ROOT-007
- REQ-ROOT-008
- REQ-ROOT-010
- REQ-ROOT-011
- REQ-ROOT-012
- REQ-ROOT-013
- REQ-ROOT-014
- REQ-ROOT-015
- REQ-ROOT-020
- REQ-UX-042
- REQ-UX-043
- REQ-UX-044
- REQ-UX-045
- ADR-ROOT-003
- ADR-ROOT-005
- ADR-ROOT-006
- ADR-ROOT-007
- ADR-ROOT-008
- ADR-ROOT-009
- ADR-UX-001
- ADR-UX-003
- ADR-UX-004
- ADR-UX-005
- ADR-UX-008
- ADR-UX-009
- ADR-UX-020
- ADR-UX-021

Target repository shape:

- `reference/` for the legacy reference crates
- `crates/` for new Rust workspace members published to `crates.io`
- `python/` for the Python package and generated Pydantic models
- `dotnet/` for the C# wrapper/package and `Directory.Build.props`

Cross-cutting release rule:

- all shipped artifact versions come from one machine-readable source of truth and are verified by normal tests and CI

## Phases

| Phase | Focus | Depends On | Status |
|---|---|---|---|
| [Phase A](phase-A/phase-A-foundation-and-deliverable-bootstrap.md) | Foundation, repo layout, workspace, catalog/codegen contract, ABI contract, naming contract, dev workflow | None | `Done` |
| [Phase B](phase-B/phase-B-core-quantity-model.md) | Core quantity model, conversions, arithmetic, array and buffer model | Phase A | `In Progress` |
| [Phase C](phase-C/phase-C-serialization-and-binary-contract.md) | JSON schema, binary format, layout and conformance rules | Phase B | `Not Started` |
| [Phase D](phase-D/phase-D-interop-surfaces.md) | C ABI, C# Interoptopus surface, Go and C interop examples | Phases B-C | `Not Started` |
| [Phase E](phase-E/phase-E-python-integration.md) | PyO3/maturin scalar and buffer APIs plus Pydantic models | Phases B-C | `Not Started` |
| [Phase F](phase-F/phase-F-validation-documentation-and-release.md) | Parity, footprint validation, docs, examples, and release readiness | Phases D-E | `Not Started` |

## Execution Model

- Phase A is the main prerequisite phase.
- Phase A must end with real delivery scaffolds present and the required lint/build/test baseline green for the shipped scope.
- Sprint dependency lists are the authoritative executable DAG. Phase dependency rows are coarse thematic ordering only.
- Sprint plans must follow `.claude/skills/plan-hardening/sprint-planning-guidelines.md`.
- Within each phase, some sprints are serial and some can run in parallel.
- Phase D and Phase E are intentionally separable after the core model and serialization contract are stable.
- Phase F consolidates cross-language validation and release readiness.
- Version-lock verification starts in Phase A and remains part of the standard validation path through Phase F.

## Completion Criteria

The project plan is complete when:

1. All phase docs exist and accurately reflect current scope and dependencies.
2. Every phase has sprint-level decomposition with explicit status.
3. The master plan and phase plans stay synchronized as execution progresses.
4. The plan explicitly covers crates.io, PyPI/pip, and NuGet publication readiness plus shared-version enforcement.
