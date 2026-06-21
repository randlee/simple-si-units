# Sprint E-4: Python Packaging And Examples

## Goal

Close Python packaging, install-flow, and example usability work for the first
publish line.

## Status

`Not Started`

## Scope References

- REQ-ROOT-014
- REQ-ROOT-016
- REQ-UX-030
- REQ-UX-031
- REQ-UX-033
- NFR-UX-011
- NFR-UX-012
- ADR-ROOT-007

## Deliverables

1. Packaging examples
2. Integration-oriented example usage docs for scalar and bulk APIs
3. PyPI/pip publication readiness
4. `maturin` build and install workflow documentation

## Dependencies

- Sprint E-3

## Unblocks

- Sprint F-4

## Acceptance Criteria

1. Python examples are executable or test-backed.
2. Packaging metadata is synchronized with the shared version source.
3. `maturin` build and install steps are explicit and reproducible from normal repo tooling.
4. The Python package is structurally ready for `pip install`-oriented release-readiness checks.

## Required Validation

1. `maturin` build/install validation succeeds for the package baseline.
2. Package installation is validated from the built artifact rather than source-tree-only imports.
3. Version synchronization reaches the Python packaging metadata targets.
4. Example snippets are executable or test-backed.
