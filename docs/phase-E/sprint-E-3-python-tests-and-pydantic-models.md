# Sprint E-3: Python Tests And Pydantic Models

## Goal

Finalize Python-facing validation and generated Pydantic model parity for the
canonical JSON contract.

## Status

`Not Started`

## Scope References

- REQ-ROOT-017
- REQ-UX-012
- REQ-UX-014
- REQ-UX-015
- REQ-UX-016
- REQ-UX-032
- REQ-UX-033
- NFR-UX-007
- NFR-UX-013
- ADR-ROOT-007
- ADR-UX-014

## Deliverables

1. Python tests covering scalar APIs, bulk APIs, and canonical JSON round-trips
2. Pydantic model generation for the canonical JSON types
3. Generated Pydantic models shipped from `python/<package>/models/generated/`
4. Canonical fixture parity tests for the generated models

## Dependencies

- Sprints A-5, E-1, E-2

## Unblocks

- Sprint E-4
- Sprint F-3

## Acceptance Criteria

1. Python-facing tests cover scalar APIs, bulk APIs, and canonical JSON round-trips.
2. Pydantic model generation is wired into the Python package structure and shipped under the planned production path.
3. Generated models serialize and deserialize canonical fixtures without shape drift.
4. The generated model set covers scalar, small-buffer, and encoded-buffer canonical JSON forms.

## Required Validation

1. Pydantic models serialize and deserialize canonical fixtures without shape drift.
2. Dedicated tests verify generated model imports from the shipped package path.
3. Dedicated tests cover scalar-versus-buffer model generation.
4. Dedicated tests cover large-buffer JSON envelope handling.
