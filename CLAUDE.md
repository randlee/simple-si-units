# Claude Instructions for units-x

## Branch Management Rules

This repository is using a `develop`-first workflow.

- Keep the main repository checkout on `develop`.
- Do not commit directly to `main` remotely.
- Use worktrees for isolated feature or review branches when needed.
- Create worktrees from `develop`, not from `main`.
- Normal incremental work lands on `develop`.
- Promote `develop` to `main` by PR when the integration state is ready.

## Project Overview

`units-x` is building a new unit-preserving quantities platform with:

- minimum storage footprint
- catalog-driven unit and type generation
- stable C ABI
- JSON and binary serialization contracts
- clean interop surfaces for Rust, C, C#, Go, and Python

The legacy `simple-si-units*` crates are not the product deliverable for this
effort. They live under `reference/` as:

- reference implementations
- conversion-factor sources
- operator-relationship sources
- regression and parity oracles

The shipped design is expected to land under `crates/`, with companion
language surfaces under `python/` and `dotnet/`.

## Key Documentation

Read these as needed:

- `docs/team-protocol.md`
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/crates/units-x/requirements.md`
- `docs/crates/units-x/architecture.md`
- `docs/prd.md`
- `docs/prd-python.md`
- `docs/prd-interop.md`
- `docs/project-plan.md`

Phase and sprint execution details live under:

- `docs/phase-A/`
- `docs/phase-B/`
- `docs/phase-C/`
- `docs/phase-D/`
- `docs/phase-E/`
- `docs/phase-F/`

Rust development guidance:

- `.claude/skills/rust-development/SKILL.md`
- `.claude/skills/rust-best-practices/SKILL.md`

Repo-local coordination and review skills:

- `.claude/skills/team-lead/SKILL.md`
- `.claude/skills/codex-orchestration/SKILL.md`
- `.claude/skills/plan-hardening/SKILL.md`
- `.claude/skills/quality-management-gh/SKILL.md`
- `.claude/skills/sprint-report/SKILL.md`

## Repository Shape

Expected top-level ownership:

- `reference/` legacy reference crates only
- `crates/` shipped Rust workspace members
- `python/` Python package, bindings, and generated models
- `dotnet/` C# wrapper/package
- `docs/` requirements, architecture, PRDs, plans, and investigation docs
- `.claude/` repo-local orchestration skills, agents, and templates

## Key Technical Rules

- The master unit catalog is intended to become the source of truth for units,
  conversions, JSON type ids, ABI naming inputs, and test generation inputs.
- The root `docs/requirements.md` and `docs/architecture.md` files are index
  documents. Crate-specific numbered `REQ-*`, `NFR-*`, and `ADR-*` ids live in
  the corresponding crate folders under `docs/crates/`.
- Design docs and planning/sprint docs should cite those numbered ids instead
  of inventing parallel unnamed requirements or architectural decisions.
- Public interop and serialization contracts must stay aligned with
  `docs/prd.md`, `docs/prd-python.md`, and `docs/prd-interop.md`.
- The product design is unit-preserving and storage-minimal; avoid drifting
  back toward canonical-SI-only storage as the public model.
- Cross-platform behavior matters. Avoid implicit text encodings, hardcoded
  Unix-only paths, and platform-specific automation assumptions.
- Keep `reference/` out of new feature ownership unless the task is explicitly
  about parity, extraction, or investigation.

## Team Configuration

- Team: `unit-x`
- Key teammates:
  - `team-lead`
  - `cunit`
  - `quality-mgr`

Use `docs/team-protocol.md` as the source of truth for required
acknowledgement and completion behavior.
