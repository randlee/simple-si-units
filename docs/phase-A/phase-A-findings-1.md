# Phase A Findings 1

## Scope

This document records the phase-ending QA findings for `integrate/phase-A` at
commit `a279ab3` during the final integration review against
`origin/develop...integrate/phase-A`.

## Traceability

- Root plan: [project-plan.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/project-plan.md)
- Phase plan: [phase-A-foundation-and-deliverable-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-foundation-and-deliverable-bootstrap.md)
- Sprint plans: [sprint-A-2-reference-extraction-and-codegen-reuse-plan.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-2-reference-extraction-and-codegen-reuse-plan.md), [sprint-A-3-abi-and-unit-naming-contract.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-3-abi-and-unit-naming-contract.md), [sprint-A-4-ci-baseline-and-dev-workflow.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-4-ci-baseline-and-dev-workflow.md), [sprint-A-5-catalog-and-generation-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-5-catalog-and-generation-bootstrap.md)
- Prior sprint findings: [sprint-A-4-findings-1.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-4-findings-1.md), [sprint-A-5-findings-1.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/sprint-A-5-findings-1.md)
- Prior fix plan: [phase-A-qa-fix-plan-1.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-qa-fix-plan-1.md)
- Product baseline: [prd.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd.md), [prd-python.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-python.md), [prd-interop.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/prd-interop.md)
- Requirements index: [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/requirements.md)
- Architecture index: [architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/architecture.md)
- `units-x` requirements: [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/requirements.md)
- `units-x` architecture: [architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/architecture.md)
- Inventory baseline: [in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/in-scope-type-inventory.md)

Relevant requirement and ADR ids for this findings set:

- `REQ-ROOT-010`
- `REQ-ROOT-011`
- `REQ-ROOT-020`
- `REQ-UX-029`
- `REQ-UX-030`
- `REQ-UX-031`
- `REQ-UX-042`
- `REQ-UX-043`
- `REQ-UX-044`
- `NFR-UX-005`
- `NFR-UX-006`
- `ADR-ROOT-009`
- `ADR-UX-014`
- `ADR-UX-015`
- `ADR-UX-020`

## QA Summary

- `phase requirements/architecture review`: `FAIL`
- `phase Rust/CI review`: `FAIL`
- `phase TODO/flaky/boundary review`: `FAIL`
- GitHub CI for PR `#9`: `PASS`
- Merge gate: `FAIL`

## Blocking Findings

### QA-001

- Source: `phase Rust/CI review`
- Severity: `BLOCKING`
- Phase-plan impact: completion criteria 5, 6, and 7 in [phase-A-foundation-and-deliverable-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-foundation-and-deliverable-bootstrap.md)
- Traceability: `REQ-ROOT-010`, `REQ-UX-030`, `REQ-UX-031`, `NFR-UX-005`, `NFR-UX-006`, `ADR-ROOT-009`
- Evidence: [ci.yml](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/integrate/phase-A/.github/workflows/ci.yml:22)
- Finding: the CI workflow still uses floating GitHub Action major tags for `actions/checkout`, `actions/setup-python`, and `actions/setup-dotnet`, which violates the Phase A pinned tool/version contract.
- Required fix: pin those actions to immutable commit SHAs and treat the pins as part of the checked-in tool-version contract.

### QA-002

- Source: `phase Rust/CI review`
- Severity: `BLOCKING`
- Phase-plan impact: completion criteria 5 and 6 in [phase-A-foundation-and-deliverable-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-foundation-and-deliverable-bootstrap.md)
- Traceability: `REQ-UX-030`, `REQ-UX-031`, `NFR-UX-005`, `ADR-ROOT-009`
- Evidence: [sync_tool_versions.py](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/integrate/phase-A/scripts/sync_tool_versions.py:53), [tool-versions.json](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/integrate/phase-A/tool-versions.json:2)
- Finding: the workflow generator still hard-codes floating action refs, and `tool-versions.json` cannot model or enforce immutable GitHub Action pins.
- Required fix: add the action SHAs to `tool-versions.json`, render them from `scripts/sync_tool_versions.py`, and extend the CI baseline tests to assert the immutable refs.

### QA1-001

- Source: `phase requirements/architecture review`, `phase TODO/flaky/boundary review`
- Severity: `BLOCKING`
- Phase-plan impact: completion criteria 3 and 4 in [phase-A-foundation-and-deliverable-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-foundation-and-deliverable-bootstrap.md)
- Traceability: `REQ-UX-042`, `ADR-UX-020`
- Evidence: [project-plan.md](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/integrate/phase-A/docs/project-plan.md:21), [in-scope-type-inventory.md](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/integrate/phase-A/docs/crates/units-x/in-scope-type-inventory.md:12), [units-catalog-summary.json](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/integrate/phase-A/catalog/generated/units-catalog-summary.json:3)
- Finding: the authoritative docs say the MVP catalog/generated surface covers the full `base`, `geometry`, `mechanical`, and `electromagnetic` families plus `Diopter`, but the committed generated catalog only exposes six dimensions.
- Required fix: either expand the catalog and generators to the documented MVP inventory, or get an explicit scope reduction approved and update the authoritative docs and requirements to match the narrower Phase A baseline.

### QA1-002

- Source: `phase requirements/architecture review`, `phase TODO/flaky/boundary review`
- Severity: `BLOCKING`
- Phase-plan impact: completion criteria 3 and 4 in [phase-A-foundation-and-deliverable-bootstrap.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/phase-A/phase-A-foundation-and-deliverable-bootstrap.md)
- Traceability: `REQ-UX-043`, `REQ-UX-044`, `ADR-UX-015`
- Evidence: [units-catalog.json](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/integrate/phase-A/catalog/units-catalog.json:297), [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/integrate/phase-A/docs/crates/units-x/requirements.md:213), [prd.md](/Volumes/Extreme%20Pro/github/simple-si-units-worktrees/integrate/phase-A/docs/prd.md:285)
- Finding: `Diopter` is modeled as its own `base` dimension in the master catalog even though the documented contract requires it to be a first-class public quantity mapped to inverse distance.
- Required fix: remodel `Diopter` in the catalog as a reciprocal/inverse-distance public type, regenerate derived artifacts, and add a regression test that asserts the inverse-distance mapping.

## Notes

- The integrated branch is structurally clean and all Phase A sprint branch heads are contained in `integrate/phase-A`.
- PR `#9` CI is green across Linux, macOS, and Windows, but the phase still fails merge-readiness because the source-of-truth contract and documented MVP surface are not yet aligned.
- `QA-001` and `QA-002` are small direct-integration fixes.
- `QA1-001` and `QA1-002` require follow-on scope work and should be handled in a dedicated sprint/worktree rather than patched into the phase-end branch ad hoc.
