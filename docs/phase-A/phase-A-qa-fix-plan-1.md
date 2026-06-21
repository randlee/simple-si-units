# Phase A QA Fix Plan 1

## Purpose

This document turns the final QA findings for Sprint A-4 and Sprint A-5 into an execution plan that can be assigned and tracked without re-deriving scope from the QA output.

## Traceability

- Root plan: [project-plan.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/project-plan.md)
- Phase plan: [phase-A-foundation-and-deliverable-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-foundation-and-deliverable-bootstrap.md)
- Sprint plans: [sprint-A-4-ci-baseline-and-dev-workflow.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-4-ci-baseline-and-dev-workflow.md), [sprint-A-5-catalog-and-generation-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-5-catalog-and-generation-bootstrap.md)
- Findings: [sprint-A-4-findings-1.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-4-findings-1.md), [sprint-A-5-findings-1.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-5-findings-1.md)
- Product baseline: [prd.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd.md), [prd-python.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-python.md), [prd-interop.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-interop.md)
- Requirements index: [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/requirements.md)
- Architecture index: [architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/architecture.md)
- `units-x` requirements: [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/requirements.md)
- `units-x` architecture: [architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/architecture.md)

Primary controlling ids:

- `REQ-ROOT-010`
- `REQ-ROOT-011`
- `REQ-ROOT-020`
- `REQ-UX-009`
- `REQ-UX-017`
- `REQ-UX-018`
- `REQ-UX-021`
- `REQ-UX-022`
- `REQ-UX-029`
- `REQ-UX-031`
- `REQ-UX-032`
- `REQ-UX-033`
- `REQ-UX-034`
- `REQ-UX-035`
- `REQ-UX-040`
- `REQ-UX-041`
- `NFR-UX-005`
- `NFR-UX-006`
- `NFR-UX-009`
- `ADR-ROOT-005`
- `ADR-ROOT-009`
- `ADR-UX-003`
- `ADR-UX-004`
- `ADR-UX-005`
- `ADR-UX-010`
- `ADR-UX-011`
- `ADR-UX-012`
- `ADR-UX-014`
- `ADR-UX-015`

## Execution Order

1. Fix Sprint A-4 blocking validation-lane issues first.
2. Re-run Sprint A-4 QA and CI.
3. Merge the corrected A-4 baseline forward into Sprint A-5.
4. Fix Sprint A-5 blocking catalog and generator issues.
5. Fix Sprint A-5 metadata-sync and important test/FFI findings in the same pass where practical.
6. Re-run Sprint A-5 QA and CI.

## Workstream A4-1: Restore Non-Mutating Tool-Version Verification

- Findings addressed: `ARCH-001`, `ARCH-002`
- Scope: [run_tests.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/.just/run_tests.py:55), [run_generate.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/.just/run_generate.py:18), [sync_tool_versions.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/scripts/sync_tool_versions.py:27), [tool-versions.json](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/tool-versions.json:2), [ci.yml](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/.github/workflows/ci.yml:1)
- Required changes:
1. Restore `scripts/sync_tool_versions.py --check` to the normal validation path before mutating generation runs.
2. Keep rewrite mode available only through the explicit generation/sync lane.
3. Extend the source-of-truth metadata to include the Rust toolchain action ref.
4. Regenerate the workflow from metadata and verify the emitted workflow contains no floating tool references.
- Closure criteria:
1. Drift in `.github/workflows/ci.yml`, `python/requirements-ci.txt`, `rust-toolchain.toml`, or `global.json` causes `just test` and `just ci` to fail without rewriting files.
2. The generated workflow no longer relies on `@stable`.
3. Existing CI still passes on Linux, macOS, and Windows.

## Workstream A4-2: Tighten FFI Failure And Length Contracts

- Findings addressed: `RBP-F001`, `RBP-F002`
- Scope: [ffi_contract.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/crates/units-x/src/ffi_contract.rs:87)
- Required changes:
1. Replace the unchecked `u64 -> usize` cast with a checked conversion and stable failure return.
2. Split lossy-conversion conditions into distinguishable failure outcomes or add a secondary error-detail surface that bindings can query deterministically.
3. Add explicit tests for oversized lengths and distinct failure causes.
- Closure criteria:
1. 32-bit-host overflow cases fail explicitly instead of truncating.
2. Foreign-language callers can distinguish arithmetic overflow from ABI-metadata overflow.

## Workstream A5-1: Make Generated Catalog Artifacts Cross-Platform Stable

- Findings addressed: `ARCH-001`, `QA-002`, `FTQ-002`
- Scope: [generate_catalog_artifacts.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/scripts/generate_catalog_artifacts.py:125), [check_generated_artifacts_clean.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/scripts/check_generated_artifacts_clean.py:1), [test_catalog_generation.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/.just/tests/test_catalog_generation.py:1)
- Required changes:
1. Force LF newlines on every generated text artifact.
2. Make the artifact-cleanliness check detect newline drift byte-for-byte.
3. Add a regression test that asserts generated JSON and Rust artifacts contain no `\r\n`.
- Closure criteria:
1. Regeneration on Windows does not alter committed artifacts solely because of line endings.
2. The cleanliness check fails if CRLF sneaks into generated outputs.

## Workstream A5-2: Correct The Catalog Wire-Shape Model

- Findings addressed: `ARCH-002`
- Scope: [units-catalog.json](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/catalog/units-catalog.json:18), [units-catalog-summary.json](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/catalog/generated/units-catalog-summary.json:1), [catalog_metadata.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/generated/catalog_metadata.rs:1)
- Required changes:
1. Replace the single `default_encoding` model with separate catalog-owned classification for scalar form, small-array form, and large-buffer form.
2. Encode the compact large-buffer envelope contract in the catalog model rather than leaving it implicit.
3. Regenerate summary and Rust metadata artifacts from the corrected catalog.
4. Add tests that prove the catalog classification covers one scalar type and one buffer-capable type exactly as required by the sprint plan.
- Closure criteria:
1. Catalog metadata can represent the PRD scalar object form, JSON array form, and compact buffer form independently.
2. Generated artifacts expose that classification without manual patching.

## Workstream A5-3: Remove Competing Manual ABI Naming Sources

- Findings addressed: `ARCH-003`, `RBP-F002`
- Scope: [ffi_contract.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/ffi_contract.rs:9), [catalog_metadata.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/generated/catalog_metadata.rs:4), [lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/lib.rs:24)
- Required changes:
1. Generate ABI-facing naming exemplars from catalog-owned naming fields, or make placeholders internal until generation owns them.
2. Reduce public comparisons against raw catalog strings where typed wrappers or typed constants are appropriate.
3. Keep the naming contract aligned with `REQ-UX-040`, `ADR-UX-010`, and `ADR-UX-012`.
- Closure criteria:
1. No public ABI naming exemplar remains hand-maintained outside catalog-owned generation inputs.
2. Public catalog identity use is typed or centralized enough to prevent manual drift.

## Workstream A5-4: Synchronize Boundary And Sprint Metadata

- Findings addressed: `SC-QA-001`, `SC-QA-002`, `ARCH-004`
- Scope: [planning.toml](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/boundaries/planning.toml:2), [core-surface.toml](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/boundaries/units-x/core-surface.toml:16), [lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/lib.rs:6)
- Required changes:
1. Advance the planning sentinel to the actual sprint state, or formally remove sprint-state coupling from the boundary record.
2. Align the boundary inventory with the real exported crate surface.
3. If `quantity` is intended to be a shipped root in Phase A, expose it and add boundary/tests accordingly. If not, remove it from the shipped-scope boundary record now.
- Closure criteria:
1. Boundary metadata matches the actual Phase A shipped surface.
2. Boundary tooling copies only accurate metadata into the scoped workspace.

## Workstream A5-5: Harden FFI Error And Test Contracts

- Findings addressed: `QA-001`, `RBP-F001`, `FTQ-001`, `RBP-F003`
- Scope: [ffi_contract.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/ffi_contract.rs:84), [test_run_tests.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/.just/tests/test_run_tests.py:27), [validate_catalog_contract.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/scripts/validate_catalog_contract.py:18)
- Required changes:
1. Apply the checked FFI length fix from Sprint A-4.
2. Add an FFI-safe error-description or recovery channel for foreign callers.
3. Isolate git config and hooks in the temp-repo test so signing and hook state cannot leak in.
4. Give catalog-validation failures stable error codes or a machine-readable failure envelope suitable for automation.
- Closure criteria:
1. FFI callers can recover from failures without reverse-engineering Rust internals.
2. Temp-repo tests are deterministic under signed-commit or custom-hook environments.
3. Tooling failures are stable enough for CI and wrapper scripts to classify.

## Validation Plan

1. Re-run `just test` and `just ci` on the corrected `A-4` branch.
2. Merge corrected `A-4` into `A-5`.
3. Re-run `just test` and `just ci` on corrected `A-5`.
4. Re-run the full QA reviewer set against the new heads:
- `req-qa`
- `arch-qa`
- `rust-qa-agent`
- `rust-best-practices-agent`
- `flaky-test-qa`
5. Confirm GitHub CI remains green on Linux, macOS, and Windows for both PRs after the fixes.

## Exit Condition

Phase A is ready for final review only when:

1. Sprint A-4 has no blocking QA findings.
2. Sprint A-5 has no blocking QA findings.
3. The important findings above are either fixed in the same pass or explicitly re-reviewed and accepted as non-blocking by project leadership.
