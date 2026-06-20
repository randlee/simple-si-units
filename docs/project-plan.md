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

The existing `simple-si-units` crates remain reference and validation oracles under `reference/`, not the primary deliverable.

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
| [Phase A](phase-A/phase-A-foundation-and-deliverable-bootstrap.md) | Foundation, repo layout, workspace, catalog/codegen contract, ABI contract, naming contract, dev workflow | None | `Not Started` |
| [Phase B](phase-B/phase-B-core-quantity-model.md) | Core quantity model, conversions, arithmetic, array and buffer model | Phase A | `Not Started` |
| [Phase C](phase-C/phase-C-serialization-and-binary-contract.md) | JSON schema, binary format, layout and conformance rules | Phase B | `Not Started` |
| [Phase D](phase-D/phase-D-interop-surfaces.md) | C ABI, C# Interoptopus surface, Go and C interop examples | Phases B-C | `Not Started` |
| [Phase E](phase-E/phase-E-python-integration.md) | PyO3/maturin scalar and buffer APIs plus Pydantic models | Phases B-C | `Not Started` |
| [Phase F](phase-F/phase-F-validation-documentation-and-release.md) | Parity, footprint validation, docs, examples, release readiness | Phases D-E | `Not Started` |

## Execution Model

- Phase A is the main prerequisite phase.
- Phase A must end with real delivery scaffolds present and the required lint/build/test baseline green for the shipped scope.
- Sprint dependency lists are the authoritative executable DAG. Phase dependency rows are coarse thematic ordering only.
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
