# Sprint F-4: Release Readiness And Publication Dry Run

## Goal

Close the release-readiness work for the initial publish line.

## Status

`Not Started`

## Scope References

- REQ-ROOT-010
- REQ-ROOT-011
- REQ-ROOT-014
- REQ-ROOT-015
- REQ-UX-030
- REQ-UX-031
- NFR-UX-011
- NFR-UX-012

## Deliverables

1. Release checklist
2. Initial publish readiness review
3. Publication dry-run checklist for `crates.io`, PyPI/pip, and `nuget.org`
4. Shared-version lock verification in release readiness
5. Rust crate packaging and `crates.io` publication readiness

## Dependencies

- Sprints F-1, F-2, F-3

## Acceptance Criteria

1. Release checklist items are explicit and complete for Rust, Python, and `.NET`.
2. Publication dry-run steps are documented for `crates.io`, PyPI/pip, and `nuget.org`.
3. Release artifacts agree on one synchronized version.
4. The first publish line (`0.1.0`) is reflected consistently in release-readiness expectations.

## Required Validation

1. Version-lock verification is run as part of release-readiness checks.
2. Dry-run packaging commands complete successfully for the shipped surfaces.
3. Final readiness review confirms no unresolved contract drift across Rust, Python, and C# deliverables.
