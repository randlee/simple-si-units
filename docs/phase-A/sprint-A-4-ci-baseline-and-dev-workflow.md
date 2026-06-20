# Sprint A-4: CI Baseline And Dev Workflow

## Goal

Create a repeatable build and test baseline for the new crate and workspace.

## Status

`Not Started`

## Deliverables

1. Baseline CI jobs
2. Standard local dev commands
3. Minimal test matrix for Linux, macOS, and Windows where practical
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

## Exit Criteria

1. Baseline build passes in CI for the new workspace shape.
2. Standard developer entrypoints are documented and stable.
3. `just test` and the default CI path fail on version drift across Rust, Python, and `.NET` package metadata.
4. The Phase A shipped scope has passing `sc-lint check`, `sc-lint clippy`, and `sc-lint-boundary` results, with legacy reference-only debt either fixed or explicitly excluded from that baseline by documented boundary.
