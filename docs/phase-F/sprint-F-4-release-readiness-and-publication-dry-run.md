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
- REQ-ROOT-017
- REQ-ROOT-018
- REQ-ROOT-019
- REQ-ROOT-021
- REQ-UX-032
- REQ-UX-030
- REQ-UX-031
- REQ-UX-033
- NFR-UX-011
- NFR-UX-012
- NFR-UX-013

## Deliverables

1. Release checklist
2. Initial publish readiness review
3. Publication dry-run checklist for `crates.io`, PyPI/pip, and `nuget.org`
4. Shared-version lock verification in release readiness
5. Rust crate packaging and `crates.io` publication readiness
6. Python wheel/sdist readiness and install verification
7. `.NET` package readiness and NuGet metadata verification
8. Cross-language artifact inventory signoff tying packages, fixtures, generated artifacts, and versions together

## Dependencies

- Sprints F-1, F-2, F-3

## Acceptance Criteria

1. Release checklist items are explicit and complete for Rust, Python, and `.NET`.
2. Publication dry-run steps are documented for `crates.io`, PyPI/pip, and `nuget.org`.
3. Release artifacts agree on one synchronized version.
4. The first publish line (`0.1.0`) is reflected consistently in release-readiness expectations.
5. No shipped package path, canonical fixture, generated artifact, or publication target remains outside the final readiness inventory.

## Required Validation

1. Version-lock verification is run as part of release-readiness checks.
2. Dry-run packaging commands complete successfully for the shipped surfaces.
3. Final readiness review confirms no unresolved contract drift across Rust, Python, and C# deliverables.
4. Validation confirms canonical JSON fixtures, binary fixtures, generated bindings, and package metadata all agree on shipped surface identifiers and versions.
