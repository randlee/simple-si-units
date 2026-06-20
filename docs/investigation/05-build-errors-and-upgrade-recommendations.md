# Build Errors And Upgrade Recommendations

## Executive summary

There are three separate issues here:

1. `cargo test` fails by default because feature-specific tests are compiled even when the corresponding optional features are disabled.
2. The crate emits a real configuration warning because `num-rational` is referenced in `cfg(feature = "...")` but is not declared as a feature.
3. This checkout is not wired as a workspace, and the main crate currently depends on the published `simple-si-units-core` and `simple-si-units-macros` crates from crates.io rather than the local reference crates now housed under `reference/`.

For a maintained fork, item 3 is the first thing I would fix. Otherwise you can easily end up modifying local crate code that the main crate is not actually compiling against.

## What I verified

Observed locally:

- `cargo test --quiet` fails in `simple-si-units`
- `cargo check --all-targets --all-features` passes
- `cargo test --all-features --quiet` passes

Also verified with `cargo metadata`:

- `simple-si-units` depends on `simple-si-units-core` and `simple-si-units-macros` from `registry+https://github.com/rust-lang/crates.io-index`, not from the local `reference/` directories in this checkout

## Root cause 1: default test failures are feature-wiring failures

The library has optional features for:

- `serde`
- `uom`
- `num-bigfloat`
- `num-complex`

See [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:23).

However, unit tests inside [simple-si-units/src/lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/lib.rs:1) unconditionally compile feature-specific numeric test code.

Representative failing test blocks:

- [test_bigfloat_unit_conversions](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/lib.rs:2289)
- complex-number cases near [src/lib.rs:4085](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/lib.rs:4085)

Why it fails:

- `num-bigfloat` and `num-complex` are present as `dev-dependencies`, so the test code can reference those types
- but the library’s optional operator impls for those types are only compiled when the corresponding crate features are enabled
- default `cargo test` does not enable those features

So the tests compile against types that exist, while the library impls they expect do not.

## Root cause 2: the generic `div_check` helper amplifies failures into a huge error flood

The helper at [simple-si-units/src/lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/lib.rs:165) requires a broad matrix of owned and borrowed `Div` impls:

```rust
A: Div<B, Output = X> + Div<&B, Output = X>
&A: Div<B, Output = X> + Div<&B, Output = X>
```

Once an optional numeric/operator implementation is missing, that helper causes a large cascade of trait-bound errors instead of a single targeted failure.

That is why the default build produces thousands of errors, even though the underlying issue is narrower.

## Root cause 3: undeclared `num-rational` feature

The main crate checks:

- [simple-si-units/src/lib.rs:55](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/lib.rs:55)

```rust
#[cfg(feature="num-rational")]
extern crate num_rational;
```

But `num-rational` is not declared in the main manifest’s optional dependencies or features:

- [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:17)

That yields the `unexpected cfg condition value: num-rational` warning on build.

The README comparison table still claims partial `num-rational` support:

- [simple-si-units/README.md](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/README.md:162)

## Root cause 4: local fork development is pointed at crates.io instead of the local reference crates

The main crate uses registry dependencies:

- [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:19)
- [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:20)

while the local path alternatives are commented out:

- [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:21)
- [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:22)

The proc-macro crate has the same pattern for `simple-si-units-core`:

- [simple-si-units-macros/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units-macros/Cargo.toml:20)
- [simple-si-units-macros/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units-macros/Cargo.toml:21)

This is the wrong setup for an active fork.

## Minimum viable fix plan

### 1. Convert the repo into a real Cargo workspace

Recommended first:

- add a root `Cargo.toml` workspace
- make `simple-si-units`, `simple-si-units-core`, and `simple-si-units-macros` workspace members
- switch internal dependencies to `path` or workspace dependencies

Why this comes first:

- otherwise your fork can silently test against published crates instead of local `reference/` changes

### 2. Gate feature-specific tests

Recommended next:

- put `#[cfg(feature = "num-bigfloat")]` on BigFloat-specific tests
- put `#[cfg(feature = "num-complex")]` on Complex-specific tests
- do the same for `uom`-specific test modules where relevant

Best target:

- gate the entire test functions, not just imports, so default `cargo test` becomes green

### 3. Decide the `num-rational` story

Pick one:

1. remove the dead `cfg(feature = "num-rational")` reference and README claim
2. or actually add optional `num-rational` support and tests

For a cleanup-focused fork, removing the dead hook is the simpler first move.

### 4. Reduce error fan-out in test helpers

Optional but worthwhile:

- simplify generic test helpers like `div_check`
- or replace some giant matrix tests with narrower explicit assertions

This will make future upgrade failures much easier to diagnose.

## Dependency recommendations

## High priority

### Internal crates: use workspace/path dependencies

This is more important than any third-party version bump.

Current issue:

- the fork is structurally set up like a consumer of published crates, not like a multi-crate workspace under active development

Recommendation:

- move internal crate versioning and dependency wiring under one workspace

### `uom`

Current main crate dependency:

- [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:25) uses `uom = "0.34"`

Current crates index result observed locally:

- `uom = "0.38.0"`

Recommendation:

- plan a deliberate upgrade from `0.34` to `0.38`

Likely breakage hotspot:

- all `uom` conversion impls and integration tests
- search surface includes [simple-si-units/tests/uom_integration_tests.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/tests/uom_integration_tests.rs:1)

### `syn`

Current proc-macro dependency:

- [simple-si-units-macros/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units-macros/Cargo.toml:23) uses `syn = "1.0"`

Current crates index result observed locally:

- `syn = "2.0.118"`

Recommendation:

- upgrade the proc-macro crate to `syn 2`

Why:

- `syn 1` is the clearest stale major dependency in the repo
- macro crates are common friction points in modern Rust upgrades

Likely breakage hotspot:

- parsing code in [simple-si-units-macros/src/lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units-macros/src/lib.rs:1)

## Medium priority

### `macrotest`

Current dev-dependency:

- [simple-si-units-macros/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units-macros/Cargo.toml:30) uses `macrotest = "1.0"`

Current crates index result observed locally:

- `macrotest = "1.2.1"`

Recommendation:

- bump when you touch macro test infrastructure

Low risk because it is dev-only.

## Low priority / already broadly current by range

These are already on open semver ranges that resolve to current compatible releases:

- `serde = "1.0"`
- `num-complex = "0.4"`
- `num-bigfloat = "1.6"` currently resolves to `1.7.x`
- `quote = "1.0"`
- `proc-macro2 = "1.0"`

Recommendation:

- no urgent manifest churn needed unless you want to tighten minimum-supported versions or normalize everything in a workspace lockfile

## Suggested upgrade order for the fork

1. Create a workspace and switch internal crates to local dependencies
2. Fix default test gating so `cargo test` is green
3. Remove or implement `num-rational`
4. Upgrade `syn` in the proc-macro crate
5. Upgrade `uom` and repair integration code/tests
6. Refresh dev dependencies like `macrotest`

## Practical recommendations

If your goal is a stable maintained fork, I would optimize for:

1. reproducible local development
2. green default CI
3. fewer optional-surface surprises
4. only then broader dependency modernization

The current odd build behavior is mostly not a deep algorithmic issue. It is project wiring:

- feature-gated impls
- ungated tests
- dead feature references
- non-workspace reference crates
