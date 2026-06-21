# units-x Crate Architecture

## Scope

This document contains the numbered architectural decisions for the primary
`units-x` Rust crate.

Design docs, planning docs, and sprint docs that depend on these choices
should cite the `ADR-UX-*` ids directly.

Detailed product narrative remains in the PRDs. This file is the traceable
crate-level architectural decision surface.

## Architectural Themes

- deliverable ownership
- public quantity model
- catalog-driven generation
- contract layering
- serialization shape
- interop separation
- traceability

## Architectural Decisions

### ADR-UX-001: New Deliverable Crate

#### Decision

The primary deliverable will be a new crate architecture under `crates/`
rather than a direct in-place evolution of the legacy crates under
`reference/`.

#### Rationale

The legacy crates are valuable as:

- reference implementations
- conversion metadata sources
- parity/validation oracles

But they do not define the intended public storage, ABI, or multi-language
product shape.

#### Consequences

- new product ownership belongs under `crates/`
- `reference/` is not the main product boundary
- parity and extraction work remain important but secondary

### ADR-UX-002: Unit-Preserving Public Model

#### Decision

The public storage model is unit-preserving. Unit identity belongs at the type
or boundary level and must not be erased into canonical-SI-only public storage
as the default external representation.

#### Rationale

The target product explicitly values:

- preserved declared units
- compact stored forms
- interop-friendly explicit unit metadata

#### Consequences

- public APIs should not assume meters-only storage for every distance value
- conversion into canonical compute forms is a bridge, not the only model
- design docs should distinguish storage representation from compute representation

### ADR-UX-003: Master Catalog As Source Of Truth

#### Decision

The implementation will use a master unit catalog as the authoritative source
for unit metadata, conversion metadata, naming inputs, and generation inputs.

#### Rationale

The product direction requires low-friction extension and minimal cross-language
duplication.

#### Consequences

- unit metadata should not be broadly hand-maintained in multiple languages
- generated surfaces should derive from catalog entries
- tests should increasingly reference catalog-derived expectations

### ADR-UX-004: Layered Contract Separation

#### Decision

The architecture separates:

- Rust-internal generic quantity modeling
- stable C ABI surfaces
- language-specific ergonomic wrappers

These are related layers, but they are not the same contract.

#### Rationale

Rust ergonomics, ABI stability, and language-specific usability pull in
different directions. Treating them as one layer would overconstrain the
implementation.

#### Consequences

- internal Rust generics do not automatically define the public ABI
- C# and Python ergonomic layers may add wrappers without changing the core ABI
- documentation must call out which layer a given type belongs to

### ADR-UX-005: JSON And Binary Contracts Are Separate

#### Decision

JSON wire contracts and binary/ABI contracts are separate architectural
surfaces and must be documented independently.

#### Rationale

The same quantity concept may need:

- ergonomic JSON structure
- compact binary or ABI-safe transport

Those constraints are not identical.

#### Consequences

- ABI layout must not be assumed to be the JSON schema
- JSON DTOs may be adjacent to ABI-facing structs where needed
- design reviews should verify both layers independently

### ADR-UX-006: Reference Crates Are Oracles, Not Owners

#### Decision

The legacy crates under `reference/` act as parity and extraction oracles, not
as the architectural ownership boundary for new product features.

#### Rationale

The product must evolve beyond the compute-first legacy shape while still
leveraging its existing knowledge.

#### Consequences

- new product features should not be implemented primarily in `reference/`
- validation against `reference/` remains useful
- migration work should preserve a clear ownership boundary

### ADR-UX-007: Traceability Through Numbered IDs

#### Decision

Per-crate requirements and ADRs are the traceable ids that planning and design
documents should cite. The root docs in `docs/` are indexes, not the full
decision payload.

#### Rationale

The project has enough planning depth that unnamed prose requirements and
decisions will drift quickly across PRDs, sprint docs, and implementation work.

#### Consequences

- sprint docs should cite `REQ-UX-*`, `NFR-UX-*`, and `ADR-UX-*`
- QA and review prompts can map findings back to stable ids
- crate docs become the canonical local traceability anchor

### ADR-UX-008: Primary Crate Name And Ownership

#### Decision

The primary crate for the design is `units-x`.

#### Rationale

This is the intended user-facing Rust deliverable and the first crate that
needs detailed requirements and architectural traceability.

#### Consequences

- initial requirements and ADR numbering anchor on `UX`
- future support crates can reference `units-x` as the core model owner
- root docs should treat `units-x` as the first-class crate baseline

### ADR-UX-009: Two-Crate MVP Bias

#### Decision

The MVP plan assumes:

1. one required crate: `units-x`
2. no second deliverable crate unless a later ADR documents a concrete
   ownership boundary that `units-x` should no longer own cleanly

#### Rationale

Over-splitting early would create coordination cost without enough code to earn
the separation.

#### Consequences

- the requirements and ADR baseline start with `units-x`
- support crates require an explicit follow-on ADR before they enter the plan
- planning documents can treat additional crates as derived work, not baseline assumptions

### ADR-UX-010: Separate Human-Readable Symbols From Code-Safe Identifiers

#### Decision

The architecture separates:

- human-readable wire/display symbols
- code-safe type or unit identifiers
- binary-safe unit ids where needed

#### Rationale

Planning explicitly requires distinctions such as:

- `C` versus `degC`
- `F` versus `degF`
- `mm` versus `Mm`

#### Consequences

- catalog entries must carry more than one naming form
- code generation must not assume one identifier serves every surface
- JSON and ABI reviews should verify the intended symbol/id separation

### ADR-UX-011: Fixed-Width ABI Slice Lengths

#### Decision

Stable ABI-facing slice and buffer contracts use `u64` length fields rather
than platform-dependent `usize`.

#### Rationale

The interop plan prioritizes predictable cross-platform ABI behavior for C, C#,
Go, and Rust.

#### Consequences

- ABI docs and examples must use `u64` explicitly
- stable exported layouts should avoid leaking host-width assumptions
- conformance tests should guard this contract

### ADR-UX-012: Catalog Owns JSON/Binary Classification Metadata

#### Decision

The master catalog owns the machine-readable classification inputs for:

- inline scalar JSON
- inline small-array JSON
- encoded-buffer JSON
- binary-safe unit ids

#### Rationale

The sprint plan repeatedly treats these as source-of-truth decisions rather
than serializer heuristics.

#### Consequences

- JSON form should not depend on ad hoc runtime branching
- downstream generators can derive fixtures and bindings from the same metadata
- wire-format reviews can validate classification from catalog output

### ADR-UX-013: Arithmetic Semantics Are Explicit, Not Emergent

#### Decision

Mixed-unit arithmetic semantics must be explicitly documented, including:

- unit-preservation rules for addition/subtraction
- deterministic promotion rules for mixed storage
- the limited canonical set of derived compute bridges

#### Rationale

The product explicitly rejects undocumented combinatorial result behavior and
needs predictable cross-language semantics.

#### Consequences

- arithmetic behavior should be a documented contract, not an implementation accident
- planning and QA can cite one stable semantics source
- derived operations should remain constrained to the documented set

### ADR-UX-020: In-Scope Unit Families Extend Beyond The Minimal Foundational Set

#### Decision

The MVP catalog and generated public surfaces must cover the reference-project
unit families `base`, `geometry`, `mechanical`, and `electromagnetic`.

#### Rationale

The product goal is broad reusable engineering coverage, and once the
catalog/generation pattern works, omitting these families adds churn without
meaningful architectural simplification.

#### Consequences

- V1 scope is broader than only distance/time/temperature/velocity/acceleration
- catalog extraction and parity work must enumerate these four families
- `chemical` and `nuclear` remain separable future scope

### ADR-UX-014: Canonical Fixtures Are Core-Model Artifacts

#### Decision

Canonical JSON and binary fixtures are owned by the core `units-x` model and
serve as downstream parity artifacts for Python, C#, and other consumers.

#### Rationale

Cross-language parity requires a single place where wire expectations are
anchored.

#### Consequences

- Rust core work owns fixture truth
- downstream bindings validate against those fixtures rather than inventing local truth
- catalog and serialization changes should update fixtures as first-class artifacts

### ADR-UX-015: Master Catalog Format Is JSON

#### Decision

The master catalog is stored in-repo as machine-readable JSON.

#### Rationale

The project needs a format that is:

- easy to diff and review
- directly consumable by Rust, Python, and `.NET` tooling
- simple for end users to extend without custom editors

#### Consequences

- Phase A generation bootstrap work should produce a JSON catalog artifact
- code generation should treat the JSON catalog as authoritative input
- schema evolution must preserve deterministic generation behavior

### ADR-UX-016: `uom` Is Reference-Or-Bridge Scope, Not Core Ownership

#### Decision

`uom` may be used for compatibility bridges, comparative testing, or optional
adapter surfaces, but it is not the foundational storage, ABI, or wire-format
owner for `units-x`.

#### Rationale

The product direction depends on:

- unit-preserving storage semantics
- catalog-driven naming and generation
- stable ABI and cross-language wire contracts

Those concerns must remain owned by `units-x` rather than delegated to a
general-purpose Rust units crate.

#### Consequences

- the core quantity model, serialization contracts, and ABI layer should not
  require `uom` to exist
- `uom` integration can be added later as an adapter or parity surface
- upgrade or compatibility work involving `uom` should not redefine the core
  product contract

### ADR-UX-017: Catalog-Derived Naming Schemes Are Deterministic

#### Decision

The MVP uses deterministic naming patterns derived from catalog metadata:

- JSON type ids: `<dimension>[_<arity>]_<storage>`
- binary unit ids: `<dimension>.<unit_code_id>`
- ABI scalar type names: `<dimension>_<unit_code_id>_<storage>`
- ABI slice type names: `<abi_scalar_type>_slice` and
  `<abi_scalar_type>_slice_mut`

#### Rationale

The plan already assumes stable generated names across Rust, Python, C#, ABI
headers, and fixtures.

#### Consequences

- generators and tests can assert names mechanically
- naming drift becomes a contract failure, not a documentation mismatch
- future scheme changes require an ADR rather than ad hoc sprint-level edits

### ADR-UX-018: V1 Binary Envelopes Use Schema-Level Unit Metadata

#### Decision

V1 binary envelopes carry one unit id at the envelope/schema level. They do
not support per-element heterogeneous unit metadata.

#### Rationale

The MVP targets compact homogeneous quantity buffers rather than mixed-unit
collections.

#### Consequences

- binary buffer payloads stay compact and regular
- serializers reject heterogeneous per-element unit data for V1 envelopes
- mixed-unit collections require a different higher-level contract if added
  later

### ADR-UX-019: Potentially Lossy Storage Conversions Are Fallible

#### Decision

When a conversion can overflow or lose required precision for the destination
storage type, the API must return an explicit failure rather than silently
truncating.

#### Rationale

Minimal storage is only acceptable when conversion behavior remains predictable
and reviewable.

#### Consequences

- integer-backed conversions need explicit fallible paths when exact
  representation is not guaranteed
- tests must cover both successful and failing storage conversions
- downstream bindings need matching error propagation contracts

### ADR-UX-021: Reciprocal Quantities Become Public When They Have Domain Identity

#### Decision

Reciprocal quantities are first-class public types when they correspond to
real domain units rather than only internal algebra artifacts.

#### Rationale

Some reciprocal dimensions are operationally important in their own right.
`Diopter` is a concrete example: users need a named public quantity rather than
an abstract inverse-distance placeholder.

#### Consequences

- the catalog must allow domain naming for reciprocal quantities
- public APIs should expose domain names such as `Diopter`
- conversion logic must bridge reciprocal-domain units and their related base
  dimensions where applicable

## Traceability Notes

- Functional and non-functional requirements for this crate are defined in
  [requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/crates/units-x/requirements.md).
- Repo-wide doc structure rules are defined in
  [docs/requirements.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/requirements.md)
  and
  [docs/architecture.md](/Volumes/Extreme%20Pro/github/simple-si-units/docs/architecture.md).
