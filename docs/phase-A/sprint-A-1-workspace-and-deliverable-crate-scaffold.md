# Sprint A-1: Workspace And Deliverable Crate Scaffold

## Goal

Convert the repo into the intended multi-surface layout and create the new deliverable scaffolds.

## Status

`Done`

## Scope References

- REQ-ROOT-001
- REQ-ROOT-013
- REQ-ROOT-016
- REQ-ROOT-019
- REQ-ROOT-020
- REQ-UX-030
- REQ-UX-031
- NFR-UX-011
- NFR-UX-012
- ADR-ROOT-006
- ADR-ROOT-007
- ADR-ROOT-008
- ADR-ROOT-009
- ADR-UX-001
- ADR-UX-008
- ADR-UX-009

## Deliverables

1. Root workspace manifest
2. `crates/units-x/` crate scaffold with baseline manifest and source tree
3. `reference/` location for legacy `simple-si-units*` crates
4. `python/` scaffold for the PyO3/maturin package and generated Pydantic models, including `pyproject.toml`
5. `dotnet/` scaffold for the C# wrapper/package and `Directory.Build.props`
6. Local path or workspace dependency wiring for every intended internal Rust deliverable crate, including a dedicated Python binding crate that remains separate from the core `units-x` Rust surface
7. Baseline crate/package metadata and feature placeholders
8. Shared version source-of-truth file plus initial synchronization wiring for Cargo, Python, and `.NET` metadata

## Why

The current repository behaves like a consumer of crates.io-published internal crates. That is not acceptable for an actively maintained fork, and it also does not reflect the intended `reference/`, `crates/`, `python/`, and `dotnet/` split.

## Dependencies

- None

## Unblocks

- All later phases

## Parallelism

- Must run first in the project

## Acceptance Criteria

1. `crates/units-x/` exists with a baseline Cargo manifest and source tree.
2. `python/` contains a baseline package skeleton and `pyproject.toml`.
3. `dotnet/` contains a baseline package skeleton and `Directory.Build.props`.
4. `reference/` remains clearly separated from new deliverable ownership.
5. Workspace-local dependency wiring is explicit, does not accidentally resolve intended internal deliverables from crates.io, and keeps language-binding crates separate from the core `units-x` Rust surface.
6. The shared version source-of-truth file is present, its synchronization targets are wired, and normal repo tooling can discover the mapping from the source version to Cargo, Python, and `.NET` metadata.

## Required Validation

1. `cargo metadata` completes successfully from repo root.
2. Workspace inspection shows `crates/units-x` and the dedicated Python binding crate are part of the intended local structure while `reference/` remains outside the shipped workspace member set.
3. A dedicated test or script proves the shared version source is discoverable from normal repo tooling.
4. A dedicated test or script proves the initial synchronization wiring reaches Cargo, Python, and `.NET` metadata targets.

## Non-Closure / Out Of Scope

- Implementing the `units-x` quantity model
- Implementing conversions
- Implementing serialization contracts
