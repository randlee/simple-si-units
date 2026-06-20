# Sprint A-1: Workspace And Deliverable Crate Scaffold

## Goal

Convert the repo into the intended multi-surface layout and create the new deliverable scaffolds.

## Status

`Not Started`

## Deliverables

1. Root workspace manifest
2. `crates/units-x/` crate scaffold with baseline manifest and source tree
3. `reference/` location for legacy `simple-si-units*` crates
4. `python/` scaffold for the PyO3/maturin package and generated Pydantic models, including `pyproject.toml`
5. `dotnet/` scaffold for the C# wrapper/package and `Directory.Build.props`
6. Local path or workspace dependency wiring for internal crates where appropriate
7. Baseline crate/package metadata and feature placeholders
8. Shared version source-of-truth file scaffold and synchronization mechanism choice

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
4. The `crates/units-x`, `python/`, and `dotnet/` delivery roots all exist with baseline publishable metadata files.
5. The shared version source-of-truth file exists, its location/format are documented, and downstream synchronization paths are identified.
