# Sprint A-5 Findings 1

## Scope

This document records the final QA findings for Sprint A-5 on branch `sprint/phase-A-5-catalog-and-generation-bootstrap` at commit `3ab0101819d11e466a3c541436232b1737f29b3d` after CI passed on Linux, macOS, and Windows.

## Traceability

- Root plan: [project-plan.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/project-plan.md)
- Phase plan: [phase-A-foundation-and-deliverable-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-foundation-and-deliverable-bootstrap.md)
- Sprint plan: [sprint-A-5-catalog-and-generation-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-5-catalog-and-generation-bootstrap.md)
- Product baseline: [prd.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd.md)
- Python baseline: [prd-python.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-python.md)
- Interop baseline: [prd-interop.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-interop.md)
- Requirements index: [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/requirements.md)
- Architecture index: [architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/architecture.md)
- `units-x` requirements: [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/requirements.md)
- `units-x` architecture: [architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/architecture.md)
- Related Phase A sprint inputs: [sprint-A-3-abi-and-unit-naming-contract.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-3-abi-and-unit-naming-contract.md), [sprint-A-4-ci-baseline-and-dev-workflow.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-4-ci-baseline-and-dev-workflow.md)

Relevant requirement and ADR ids for this findings set:

- `REQ-ROOT-006`
- `REQ-ROOT-008`
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
- `REQ-UX-036`
- `REQ-UX-040`
- `REQ-UX-041`
- `NFR-UX-005`
- `NFR-UX-006`
- `NFR-UX-004`
- `NFR-UX-009`
- `ADR-ROOT-005`
- `ADR-UX-003`
- `ADR-UX-004`
- `ADR-UX-005`
- `ADR-UX-011`
- `ADR-UX-010`
- `ADR-UX-012`
- `ADR-UX-014`
- `ADR-UX-015`

## QA Summary

- `req-qa`: `FAIL`
- `arch-qa`: `FAIL`
- `rust-qa-agent`: `findings`
- `rust-best-practices-agent`: `findings`
- `flaky-test-qa`: `findings`
- GitHub CI: `PASS`
- Merge gate: `FAIL`

## Blocking Findings

### ARCH-001

- Source: `arch-qa`
- Severity: `BLOCKING`
- Sprint-plan impact: required validation 1 and 2 plus acceptance criteria 2 and 3 in [sprint-A-5-catalog-and-generation-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-5-catalog-and-generation-bootstrap.md)
- Traceability: `NFR-UX-005`, `NFR-UX-006`, `REQ-UX-029`, `ADR-UX-014`
- Evidence: [generate_catalog_artifacts.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/scripts/generate_catalog_artifacts.py:125)
- Finding: generated text artifacts are written without forcing LF newlines, so Windows regeneration can emit CRLF and evade strict drift detection.
- Required fix: write generated text artifacts with `newline="\n"` and make the cleanliness check reject newline drift explicitly.

### ARCH-002

- Source: `arch-qa`
- Severity: `BLOCKING`
- Sprint-plan impact: deliverable 5 and acceptance criterion 4 in [sprint-A-5-catalog-and-generation-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-5-catalog-and-generation-bootstrap.md)
- Traceability: `REQ-UX-017`, `REQ-UX-033`, `REQ-UX-034`, `REQ-UX-036`, `ADR-UX-012`, `ADR-UX-014`, `ADR-UX-015`
- Evidence: [units-catalog.json](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/catalog/units-catalog.json:18), [prd.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd.md)
- Finding: catalog JSON-form metadata currently collapses public JSON shape to one `default_encoding` per dimension, which cannot represent the documented split between scalar object form, small-array JSON form, and compact large-buffer form.
- Required fix: redesign the catalog JSON-form contract so scalar, small-array, and buffer forms are represented separately and regenerate derived artifacts from that richer contract.

### ARCH-003

- Source: `arch-qa`
- Severity: `BLOCKING`
- Sprint-plan impact: deliverable 5 and acceptance criterion 4 in [sprint-A-5-catalog-and-generation-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-5-catalog-and-generation-bootstrap.md)
- Traceability: `REQ-UX-009`, `REQ-UX-018`, `REQ-UX-040`, `NFR-UX-009`, `ADR-UX-003`, `ADR-UX-010`, `ADR-UX-012`
- Evidence: [ffi_contract.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/ffi_contract.rs:9), [units-catalog.json](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/catalog/units-catalog.json:1)
- Finding: public ABI naming exemplars are still hand-maintained in `ffi_contract.rs` even though naming inputs are supposed to be catalog-owned.
- Required fix: generate the public ABI naming surface from catalog metadata, or keep these names private placeholders until generated ownership exists.

## Important Findings

### SC-QA-001

- Source: `req-qa`
- Severity: `IMPORTANT`
- Traceability: `REQ-ROOT-006`, `REQ-ROOT-008`, `ADR-ROOT-005`
- Evidence: [planning.toml](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/boundaries/planning.toml:2), [phase-A-foundation-and-deliverable-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-foundation-and-deliverable-bootstrap.md)
- Finding: the planning sentinel still says `A.4`, which is inconsistent with the Sprint A-5 reviewed branch state.
- Required fix: advance the sentinel to `A.5` or stop encoding sprint state there if the boundary tooling does not need it.

### SC-QA-002

- Source: `req-qa`
- Severity: `IMPORTANT`
- Traceability: `REQ-ROOT-006`, `REQ-UX-029`, `ADR-UX-003`
- Evidence: [core-surface.toml](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/boundaries/units-x/core-surface.toml:16), [lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/lib.rs:6)
- Finding: the shipped-scope boundary inventory still lists `quantity` as a composition root even though the crate surface does not expose it.
- Required fix: either remove `quantity` from the boundary inventory or expose and implement the intended root consistently.

### QA-001

- Source: `rust-qa-agent`
- Severity: `IMPORTANT`
- Traceability: `REQ-UX-021`, `REQ-UX-041`, `NFR-UX-004`, `ADR-UX-011`
- Evidence: [ffi_contract.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/ffi_contract.rs:117)
- Finding: the FFI slice entrypoint still truncates `u64` length to `usize` with `as`.
- Required fix: use checked conversion and return a stable failure status for oversized lengths.

### QA-002

- Source: `rust-qa-agent`
- Severity: `IMPORTANT`
- Traceability: `NFR-UX-005`, `NFR-UX-006`, `REQ-UX-029`
- Evidence: [generate_catalog_artifacts.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/scripts/generate_catalog_artifacts.py:125)
- Finding: generator writes are not LF-stable across platforms.
- Required fix: same as `ARCH-001`, plus a regression test at the byte level.

### RBP-F001

- Source: `rust-best-practices-agent`
- Severity: `IMPORTANT`
- Traceability: `REQ-UX-022`, `ADR-UX-004`, `ADR-UX-005`
- Evidence: [ffi_contract.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/ffi_contract.rs:84)
- Finding: the FFI error surface exposes only numeric status codes with no stable foreign-language cause or recovery description.
- Required fix: add an FFI-safe error-description channel without changing the stable status enum contract.

### RBP-F002

- Source: `rust-best-practices-agent`
- Severity: `IMPORTANT`
- Traceability: `REQ-UX-009`, `REQ-UX-040`, `ADR-UX-003`
- Evidence: [catalog_metadata.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/generated/catalog_metadata.rs:4), [lib.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/crates/units-x/src/lib.rs:24)
- Finding: catalog-owned semantic identifiers cross the public Rust surface as raw strings rather than typed zero-cost wrappers.
- Required fix: generate typed wrappers or typed constants for public catalog identity fields.

### FTQ-001

- Source: `flaky-test-qa`
- Severity: `IMPORTANT`
- Traceability: `NFR-UX-005`, `NFR-UX-006`, `REQ-UX-031`
- Evidence: [test_run_tests.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/.just/tests/test_run_tests.py:27)
- Finding: the test shells out to real `git commit` without isolating global git config or hooks, so signing or hook setup can make it machine-dependent.
- Required fix: isolate git config for the temp repo or disable signing and hooks explicitly for the subprocesses used by the test.

### FTQ-002

- Source: `flaky-test-qa`
- Severity: `IMPORTANT`
- Traceability: `NFR-UX-005`, `NFR-UX-006`, `REQ-UX-029`
- Evidence: [generate_catalog_artifacts.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/scripts/generate_catalog_artifacts.py:125)
- Finding: newline serialization follows the host OS, which makes generated artifact comparison environment-sensitive.
- Required fix: same as `ARCH-001` and `QA-002`.

## Minor Findings

### RBP-F003

- Source: `rust-best-practices-agent`
- Severity: `MINOR`
- Traceability: `REQ-UX-029`, `REQ-UX-031`, `ADR-UX-014`
- Evidence: [validate_catalog_contract.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-5-catalog-and-generation-bootstrap/scripts/validate_catalog_contract.py:18)
- Finding: validator failures are reported through ad hoc exception text rather than a stable tooling error envelope.
- Required fix: add stable error codes and a concise machine-readable failure envelope for the catalog validation entrypoint.

## Notes

- The dedicated TODO scan did not surface a Sprint A-5 product-code TODO blocker.
- CI is green, but the sprint is still not merge-ready because the catalog, generator, and boundary contracts are not yet aligned with the documented Phase A baseline.
