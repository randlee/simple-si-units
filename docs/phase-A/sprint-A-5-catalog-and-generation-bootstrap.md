# Sprint A-5: Catalog And Generation Bootstrap

## Goal

Build the first real catalog-driven generation baseline so later phases do not depend on a purely theoretical catalog.

## Status

`Done`

## Scope References

- REQ-UX-009
- REQ-UX-017
- REQ-UX-018
- REQ-UX-029
- REQ-UX-032
- REQ-UX-034
- REQ-UX-035
- REQ-UX-040
- NFR-UX-013
- ADR-UX-003
- ADR-UX-012
- ADR-UX-014
- ADR-UX-015
- ADR-UX-017

## Deliverables

1. Initial machine-readable master catalog
2. Initial generator/bootstrap path consuming that catalog
3. At least one generated artifact or inventory committed to the repo
4. Documented regeneration entrypoint wired into local workflow
5. Machine-readable encoding-form and unit-id decisions emitted or enforced from the catalog

## Dependencies

- Sprints A-2, A-3, A-4

## Unblocks

- Sprints B-2, B-3, C-1, C-2, E-3, F-1

## Acceptance Criteria

1. The catalog is committed as a real machine-readable artifact.
2. A documented generation entrypoint runs from normal repo tooling.
3. At least one generated artifact, fixture, or inventory is committed and tied to the catalog.
4. JSON-form classification and binary-safe unit-id decisions are emitted from catalog-owned metadata.

## Required Validation

1. Regeneration from a clean checkout reproduces the committed generated artifacts.
2. A test or diff check fails when generated artifacts drift from catalog inputs.
3. Sample generated output covers at least one scalar type and one buffer-capable type.
4. Dedicated regeneration tests cover case-sensitive unit ids such as `mm` versus `Mm`, reserved identifier handling, and at least one offset-conversion catalog entry.
