# Development Workflow

## Purpose

This document records the Phase A local workflow and CI baseline for `units-x`.

## Standard Commands

- `just help`
- `just build`
- `just test`
- `just test unit`
- `just test python`
- `just test dotnet`
- `just test integration`
- `just test rust`
- `just lint full`
- `just lint sc-boundary`
- `just ci`

## Baseline Expectations

- `just test` is the full repo test pass.
- `just ci` is the strict local CI-equivalent command set.
- GitHub Actions runs the same `just ci` entrypoint on Linux, macOS, and Windows.

## Shipped-Scope Lint Boundary

Phase A enforces two different scopes on purpose:

1. Full-repo testing:
   This still covers the legacy `reference/` crates through the normal Rust
   workspace tests and helper-script tests.
2. Shipped-scope linting:
   `sc-lint check`, `sc-lint clippy`, and `sc-lint-boundary` are enforced
   against a synthetic shipped workspace containing only `crates/units-x` and
   its boundary metadata.

This exclusion exists because the legacy reference crates remain parity and
source-extraction oracles, but they are not the Phase A shipped deliverable and
they currently contain legacy patterns that are outside the intended lint
baseline.

## Enforcement Notes

- The shipped-scope Rust lint wrappers live under `.just/`.
- `boundaries/units-x/core-surface.toml` is the boundary inventory baseline for
  the shipped crate.
- `just ci` runs the shipped-scope clippy and boundary gates after the full
  repo test pass.
