# Reference Extraction And Codegen Reuse Plan

## Purpose

This document maps the current reference inputs and generator implementation to
the planned `units-x` catalog-driven generation model.

## Scope References

- REQ-UX-006
- REQ-UX-009
- REQ-UX-018
- REQ-UX-029
- REQ-UX-032
- REQ-UX-034
- REQ-UX-035
- REQ-UX-040
- NFR-UX-008
- NFR-UX-013
- ADR-UX-003
- ADR-UX-010
- ADR-UX-012
- ADR-UX-015
- ADR-UX-017

## Reference Input Mapping

| Current source | Current role | `units-x` target role | Decision | Notes |
|---|---|---|---|---|
| `code-generator/unit-type-definitions.csv` | Declares quantity families, canonical unit names, display metadata, and some `uom` metadata | Seeds dimension-level catalog entries and public-type mapping | `adapt` | The family/type information is valuable, but names and ids must be normalized to the new catalog contract. |
| `code-generator/measurement-units.csv` | Declares concrete unit symbols plus slope/offset conversion data | Seeds unit-level catalog entries and conversion metadata | `adapt` | The numeric conversion data maps cleanly, but the new catalog must split `unit_symbol`, `unit_code_id`, and `binary_unit_id`. |
| `reference/simple-si-units/src/*.rs` generated unit impls | Encodes available units, naming patterns, and parity behavior | Validation oracle and extraction backstop | `reuse` | These files remain the parity oracle for existing families and a source for inventory checks. |
| `docs/crates/units-x/in-scope-type-inventory.md` | Authoritative public-type checklist | Remains the sprint/QA checklist surface | `reuse` | This stays the closure checklist for later implementation sprints. |

## Conversion Mapping

The current reference conversion model is canonical-SI-storage-oriented:

- `measurement-units.csv` provides slope/offset values to the dimension base
- generated impls expose `from_*` and `to_*` conversions around canonical SI storage

The `units-x` catalog preserves the useful numeric data but changes ownership:

- conversion metadata moves into JSON catalog entries
- storage remains in the chosen declared unit rather than always canonical SI
- canonical compute conversions become explicit bridge operations rather than
  the only storage model

## Generator Component Classification

| Artifact or function | Current role | Decision | Rationale |
|---|---|---|---|
| `code-generator/code_generator.py:main` | End-to-end write into `reference/simple-si-units/src/*.rs` | `replace` | The output target and generated product shape are wrong for `units-x`. |
| `generate_modules` / `generate_unit_structs` | Emits reference Rust source modules | `replace` | The new crate needs catalog-driven storage/ABI/wire artifacts, not direct legacy module emission. |
| `generate_from_to_conversions` / `generate_nonconverting_from_to_conversions` | Encodes slope/offset conversion knowledge | `adapt` | The underlying conversion relationships remain useful, but the output form must become catalog data or generated conversion tables. |
| `generate_uom_conversions` | Emits `uom` bridge impls | `replace` | `uom` is adapter/parity scope rather than core ownership in `units-x`. |
| `find_unit_conversions` / operator graph discovery | Derives multiplication/division relationships | `adapt` | The derivative relationship knowledge is valuable, but the MVP arithmetic scope is narrower and must not inherit the full legacy operator graph by accident. |
| `recommend_unit_tests` | Emits reference-project test cases | `adapt` | The idea transfers, but the new project should generate catalog-owned fixtures and targeted conformance tests instead. |
| `post_gen_patching` | Cleans generator output with string post-processing | `replace` | The new pipeline should not depend on ad hoc source rewriting after generation. |
| `templates.py` | Legacy Rust source templates | `replace` | New outputs span Rust, fixtures, Python, and C# inputs. |

## Mapping Notes For The In-Scope Inventory

The in-scope inventory already lists the required public families:

- `base`
- `geometry`
- `mechanical`
- `electromagnetic`
- `Diopter`

Important mapping notes:

- `AreaPerLumen` maps to the reference quantity named `area per lumen`
- `VolumePerMass` maps to the reference quantity named `volume per mass`
- `Diopter` is a `units-x` addition and does not come from the reference CSVs
- `chemical` and `nuclear` rows remain out of MVP scope and are not required to
  close Phase A

## First Generated Outputs Planned From This Reuse Model

The first generation bootstrap should own:

- a committed JSON catalog
- a generated inventory/registry artifact tied to that catalog
- generated Rust registry or conversion-table inputs
- drift checks proving catalog-owned generated files are current

## Extension Workflow

When a maintainer or end user adds a unit later, the intended workflow is:

1. Add or edit the unit in the JSON catalog.
2. Regenerate artifacts.
3. Run `just test`.
4. Review generated changes for the affected dimension/type surfaces.

Manual edits to every language surface are explicitly not the intended path.
