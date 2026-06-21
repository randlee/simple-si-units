# Sprint A-4: CI Baseline And Dev Workflow

## Goal

Create a repeatable build and test baseline for the new crate and workspace.

## Status

`In Progress`

## Scope References

- REQ-UX-030
- REQ-UX-031
- NFR-UX-005
- NFR-UX-011
- NFR-UX-012

## Deliverables

1. Baseline CI jobs
2. Standard local dev commands
3. Minimal test matrix covering Linux, macOS, and Windows for the shipped scope
4. Formatting and linting baseline
5. Shared-version drift check included in normal test entrypoints
6. Required `sc-lint` baseline for the shipped scope

## Why

The new crate must not repeat the ambiguous build behavior of the current project.

## Dependencies

- Sprint A-1

## Unblocks

- All implementation phases

## Parallelism

- Can run in parallel with Sprints A-2 and A-3

## Acceptance Criteria

1. Baseline build and test entrypoints are documented and runnable from repo root.
2. CI includes Linux, macOS, and Windows coverage for the shipped scope.
3. `just test` includes generation, version-lock verification, linting, Rust tests, Python wheel smoke, and `.NET` scaffold validation.
4. The Phase A shipped scope has an explicit lint baseline, including any documented exclusions for legacy reference-only debt.
5. Platform-sensitive generation or serialization helpers document their encoding/path assumptions explicitly.
6. CI installs pinned tool and package versions rather than floating channels.

## Required Validation

1. `just test` fails on version drift.
2. CI baseline exercises Windows text/encoding-sensitive paths.
3. `sc-lint check`, `sc-lint clippy`, and `sc-lint-boundary` are either green for the shipped scope or the exclusion boundary is documented and enforced.
4. The Python publish lane can build a wheel from `python/` and import `units_x._native`.

## Edge / Corner Conditions Requiring Dedicated Tests

1. Windows text encoding behavior in generator paths.
2. Reference-only debt exclusion boundaries.
3. Empty scaffold repos where Python or `.NET` subtrees exist but have no full product code yet.

## Current Phase A Baseline Decision

Phase A uses an enforced shipped-scope lint boundary:

- full-repo tests still include `reference/`
- the full-repo pass covers `reference/` through explicit
  `cargo test --manifest-path ...` commands because those crates are excluded
  from the shipped workspace
- shipped-scope `sc-lint` and `sc-lint-boundary` gates run against a synthetic
  workspace containing `crates/units-x`, `crates/units-x-python`,
  `boundaries/units-x`, `boundaries/units-x-python`, and the required
  `boundaries/planning.toml` sentinel
- the exclusion is documented in `docs/development-workflow.md`
