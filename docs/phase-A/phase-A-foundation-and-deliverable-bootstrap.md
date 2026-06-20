# Phase A: Foundation And Deliverable Bootstrap

## Goal

Establish the new repository layout, deliverable crate location, workspace structure, master-catalog/codegen contract, ABI rules, unit naming rules, shared-version contract, and execution baseline before implementation begins.

## Status

`Not Started`

## Phase Dependencies

- None

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint A-1](sprint-A-1-workspace-and-deliverable-crate-scaffold.md) | Create `reference/`, `crates/`, `python/`, and `dotnet/` scaffold plus workspace baseline | None | None | `Not Started` |
| [Sprint A-2](sprint-A-2-reference-extraction-and-codegen-reuse-plan.md) | Define master catalog and codegen reuse plan | Sprint A-1 | Sprint A-4 | `Not Started` |
| [Sprint A-3](sprint-A-3-abi-and-unit-naming-contract.md) | Lock ABI, naming, layout, and symbol rules | Sprint A-1 | Sprint A-4 | `Not Started` |
| [Sprint A-4](sprint-A-4-ci-baseline-and-dev-workflow.md) | Create CI, test, and local workflow baseline | Sprint A-1 | Sprints A-2, A-3 | `Not Started` |

## Phase Completion Criteria

Phase A is complete when:

1. The new crate exists as the primary deliverable inside a workspace-ready structure.
2. Internal dependency wiring is local and explicit.
3. The master catalog and generation contract are documented and accepted.
4. ABI and unit-naming contracts are documented and accepted.
5. CI and local workflows can build and test the empty baseline.
6. Shared-version synchronization rules are documented and wired into baseline validation.
