# Phase A: Foundation And Deliverable Bootstrap

## Goal

Establish the new repository layout, deliverable crate location, workspace structure, master-catalog/codegen contract and bootstrap, ABI rules, unit naming rules, shared-version contract, and execution baseline before implementation begins.

## Status

`In Progress`

## Scope References

- REQ-ROOT-010
- REQ-ROOT-011
- REQ-ROOT-013
- REQ-ROOT-016
- REQ-ROOT-019
- REQ-ROOT-020
- REQ-UX-009
- REQ-UX-018
- REQ-UX-029
- REQ-UX-030
- REQ-UX-031
- REQ-UX-034
- REQ-UX-035
- NFR-UX-012
- NFR-UX-013
- ADR-ROOT-006
- ADR-ROOT-007
- ADR-ROOT-008
- ADR-ROOT-009
- ADR-UX-001
- ADR-UX-003
- ADR-UX-008
- ADR-UX-010
- ADR-UX-011
- ADR-UX-012
- ADR-UX-015

## Phase Dependencies

- None

## Sprints

| Sprint | Focus | Depends On | Parallel With | Status |
|---|---|---|---|---|
| [Sprint A-1](sprint-A-1-workspace-and-deliverable-crate-scaffold.md) | Create `reference/`, `crates/`, `python/`, and `dotnet/` scaffold plus workspace baseline | None | None | `Done` |
| [Sprint A-2](sprint-A-2-reference-extraction-and-codegen-reuse-plan.md) | Define master catalog and codegen reuse plan | Sprint A-1 | Sprint A-4 | `Done` |
| [Sprint A-3](sprint-A-3-abi-and-unit-naming-contract.md) | Lock ABI, naming, layout, and symbol rules | Sprint A-1 | Sprint A-4 | `Done` |
| [Sprint A-4](sprint-A-4-ci-baseline-and-dev-workflow.md) | Create CI, test, and local workflow baseline | Sprint A-1 | Sprints A-2, A-3 | `Done` |
| [Sprint A-5](sprint-A-5-catalog-and-generation-bootstrap.md) | Build the first catalog-driven generation baseline | Sprints A-2, A-3, A-4 | None | `In Progress` |

## Phase Completion Criteria

Phase A is complete when:

1. A concrete `crates/units-x` deliverable scaffold exists alongside `python/` and `dotnet/` publishable scaffolds.
2. Internal dependency wiring is local and explicit.
3. The master catalog and generation contract are documented and an initial generation baseline exists.
4. ABI and unit-naming contracts are documented and accepted.
5. CI and local workflows can build and test the empty baseline.
6. Shared-version synchronization rules are documented and wired into baseline validation.
7. The required Phase A `sc-lint` baseline is green for the intended shipped scope.
