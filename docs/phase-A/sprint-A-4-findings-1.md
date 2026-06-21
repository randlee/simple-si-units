# Sprint A-4 Findings 1

## Scope

This document records the final QA findings for Sprint A-4 on branch `sprint/phase-A-4-ci-baseline-and-dev-workflow` at commit `4a34d173f128965c2b1e30a4b335cd5c5ac50557` after CI passed on Linux, macOS, and Windows.

## Traceability

- Root plan: [project-plan.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/project-plan.md)
- Phase plan: [phase-A-foundation-and-deliverable-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-foundation-and-deliverable-bootstrap.md)
- Sprint plan: [sprint-A-4-ci-baseline-and-dev-workflow.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-4-ci-baseline-and-dev-workflow.md)
- Product baseline: [prd.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd.md)
- Python baseline: [prd-python.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-python.md)
- Interop baseline: [prd-interop.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-interop.md)
- Requirements index: [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/requirements.md)
- Architecture index: [architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/architecture.md)
- `units-x` requirements: [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/requirements.md)
- `units-x` architecture: [architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/architecture.md)
- Related Phase A sprint inputs: [sprint-A-3-abi-and-unit-naming-contract.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-3-abi-and-unit-naming-contract.md), [sprint-A-5-catalog-and-generation-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-5-catalog-and-generation-bootstrap.md)

Relevant requirement and ADR ids for this findings set:

- `REQ-ROOT-010`
- `REQ-ROOT-011`
- `REQ-ROOT-020`
- `REQ-UX-019`
- `REQ-UX-021`
- `REQ-UX-022`
- `REQ-UX-030`
- `REQ-UX-031`
- `REQ-UX-041`
- `NFR-UX-005`
- `NFR-UX-006`
- `NFR-UX-003`
- `NFR-UX-004`
- `ADR-ROOT-005`
- `ADR-ROOT-009`
- `ADR-UX-004`
- `ADR-UX-005`
- `ADR-UX-011`

## QA Summary

- `req-qa`: `PASS`
- `arch-qa`: `FAIL`
- `rust-qa-agent`: `PASS`
- `rust-best-practices-agent`: `findings`
- `flaky-test-qa`: `PASS`
- GitHub CI: `PASS`
- Merge gate: `FAIL`

## Blocking Findings

### ARCH-001

- Source: `arch-qa`
- Severity: `BLOCKING`
- Sprint-plan impact: acceptance criterion 3 and required validation 1 in [sprint-A-4-ci-baseline-and-dev-workflow.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-4-ci-baseline-and-dev-workflow.md)
- Traceability: `REQ-ROOT-011`, `REQ-UX-031`, `NFR-UX-005`, `ADR-ROOT-005`, `ADR-ROOT-009`
- Evidence: [run_tests.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/.just/run_tests.py:55), [run_generate.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/.just/run_generate.py:18), [sync_tool_versions.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/scripts/sync_tool_versions.py:110)
- Finding: `just test` reaches tool-version synchronization through the mutating generation lane, so drift in generated tool-version files can be rewritten instead of causing the normal validation path to fail.
- Required fix: add a non-mutating `scripts/sync_tool_versions.py --check` gate in the normal validation path and keep rewriting as an explicit maintenance step.

### ARCH-002

- Source: `arch-qa`
- Severity: `BLOCKING`
- Sprint-plan impact: deliverables 1 and 5 plus required validation 3 in [sprint-A-4-ci-baseline-and-dev-workflow.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-4-ci-baseline-and-dev-workflow.md)
- Traceability: `REQ-ROOT-010`, `REQ-UX-030`, `NFR-UX-005`, `NFR-UX-006`, `ADR-ROOT-009`
- Evidence: [sync_tool_versions.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/scripts/sync_tool_versions.py:27), [tool-versions.json](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/tool-versions.json:2)
- Finding: the generated workflow still uses `dtolnay/rust-toolchain@stable`, which is a floating install surface outside the declared pin set.
- Required fix: carry the workflow action ref in the same source-of-truth metadata and generate a non-floating workflow reference.

## Important Findings

### RBP-F001

- Source: `rust-best-practices-agent`
- Severity: `IMPORTANT`
- Traceability: `REQ-UX-022`, `ADR-UX-004`, `ADR-UX-005`
- Evidence: [ffi_contract.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/crates/units-x/src/ffi_contract.rs:87)
- Finding: distinct ABI failure causes are collapsed into one lossy-conversion status, which weakens stable foreign-language recovery behavior.
- Required fix: split the status codes or add an FFI-safe error-detail channel.

### RBP-F002

- Source: `rust-best-practices-agent`
- Severity: `IMPORTANT`
- Traceability: `REQ-UX-021`, `REQ-UX-041`, `NFR-UX-004`, `ADR-UX-011`
- Evidence: [ffi_contract.rs](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/sprint/phase-A-4-ci-baseline-and-dev-workflow/crates/units-x/src/ffi_contract.rs:117)
- Finding: the FFI slice entrypoint casts `u64` length to `usize` with `as`, which can truncate on narrower targets instead of failing explicitly.
- Required fix: use `usize::try_from(input.len)` and return a stable non-success status when conversion fails.

## Notes

- The dedicated TODO scan did not surface a Sprint A-4 product-code TODO blocker.
- `rust-qa-agent` and `flaky-test-qa` both passed the scoped review.
- This sprint should not be merged until the two blocking findings are fixed and the important FFI follow-ups are triaged into the same fix pass.
