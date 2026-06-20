# Sprint A-1: Workspace And Deliverable Crate Scaffold

## Goal

Convert the repo into the intended multi-surface layout and create the new deliverable scaffolds.

## Status

`Not Started`

## Deliverables

1. Root workspace manifest
2. `reference/` location for legacy `simple-si-units*` crates
3. `crates/` scaffold for new Rust deliverables
4. `python/` scaffold for the PyO3/maturin package and generated Pydantic models
5. `dotnet/` scaffold for the C# wrapper/package and `Directory.Build.props`
6. Local path or workspace dependency wiring for internal crates where appropriate
7. Baseline crate/package metadata and feature placeholders
8. Shared version source-of-truth file scaffold

## Why

The current repository behaves like a consumer of crates.io-published internal crates. That is not acceptable for an actively maintained fork, and it also does not reflect the intended `reference/`, `crates/`, `python/`, and `dotnet/` split.

## Dependencies

- None

## Unblocks

- All later phases

## Parallelism

- Must run first in the project

## Exit Criteria

1. `cargo metadata` reflects the intended workspace.
2. Internal crates are no longer accidentally resolved from crates.io during local development.
3. The repository layout clearly separates legacy reference crates from new shipped deliverables.
4. The shared version source-of-truth file exists and downstream package metadata paths are identified.
