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
- The Python lane includes helper-script tests plus a wheel-build/import smoke test
  for `units_x._native`.

## Shipped-Scope Lint Boundary

Phase A enforces two different scopes on purpose:

1. Full-repo testing:
   This still covers the legacy `reference/` crates through the normal Rust
   workspace tests and helper-script tests.
2. Shipped-scope linting:
   `sc-lint check`, `sc-lint clippy`, and `sc-lint-boundary` are enforced
   against a synthetic shipped workspace containing `crates/units-x`,
   `crates/units-x-python`, `boundaries/units-x`,
   `boundaries/units-x-python`, and the required
   `boundaries/planning.toml` sentinel.

This exclusion exists because the legacy reference crates remain parity and
source-extraction oracles, but they are not the Phase A shipped deliverable and
they currently contain legacy patterns that are outside the intended lint
baseline.

## Enforcement Notes

- The shipped-scope Rust lint wrappers live under `.just/`.
- `boundaries/units-x/core-surface.toml` and
  `boundaries/units-x-python/python-surface.toml` are the boundary inventory
  baselines for the shipped Rust crates.
- `just ci` runs the shipped-scope clippy and boundary gates after the full
  repo test pass.
- CI installs pinned Rust, Python, `.NET`, `just`, `sc-lint`, and
  `sc-lint-boundary` versions from checked-in workflow metadata.

## Windows / Encoding Assumptions

- Python helper scripts read and write text as UTF-8 only.
- Generated text files use LF newlines so Windows, macOS, and Linux compare the
  same serialized content in CI.
- The synthetic shipped workspace must include `crates/units-x`,
  `crates/units-x-python`, `boundaries/units-x`, and
  `boundaries/units-x-python`.
- The shipped-scope workspace helpers must work with paths containing spaces and
  native platform separators.
- GitHub Actions enforces these assumptions by running `just ci` on
  `windows-latest` with `PYTHONUTF8=1`.
