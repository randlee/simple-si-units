# units-x

`units-x` is a unit-preserving quantities project focused on compact storage, deterministic serialization, and stable cross-language interop.

This repository is currently being reshaped from a fork/reference base into the new `units-x` deliverable. The legacy `simple-si-units` crates are kept under [`reference/`](reference/) as source material, regression oracles, and migration input, but they are not the target product surface.

## Inspiration

This project was inspired by the original `simple-si-units` work:

- https://github.com/DrPlantabyte/simple-si-units

## Planned deliverables

`units-x` is intended to ship as:

- a Rust crate on `crates.io` as `units-x`
- a Homebrew package as `units-x`
- a NuGet package on `nuget.org` as `units-x`
- a Python package for normal `pip install` consumption

The first publish line is planned to start at version `0.1.0`.

## Product direction

The new design targets:

- unit-preserving storage rather than forced canonical-SI storage
- minimum footprint for scalars and arrays
- explicit JSON and binary serialization paths
- stable C ABI for Rust, C, C#, Go, and related consumers
- generated Python and `.NET` surfaces
- catalog-driven code generation and version synchronization

Detailed product and interop planning lives under [`docs/`](docs/), especially:

- [`docs/prd.md`](docs/prd.md)
- [`docs/prd-python.md`](docs/prd-python.md)
- [`docs/prd-interop.md`](docs/prd-interop.md)
- [`docs/project-plan.md`](docs/project-plan.md)

## Repository layout

- [`reference/`](reference/) contains the legacy `simple-si-units` crates
- [`crates/`](crates/) is reserved for the new Rust deliverables
- [`python/`](python/) is reserved for the Python package and generated Pydantic models
- [`dotnet/`](dotnet/) is reserved for the C# wrapper/package and `Directory.Build.props`
- [`boundaries/`](boundaries/) is the future home for `sc-lint` boundary policy files

## Local workflow

The repo now uses `just` as the primary task runner.

Common commands:

- `just help`
- `just build`
- `just test all`
- `just test unit`
- `just test python`
- `just test integration`
- `just lint full`
- `just lint sc-boundary`
- `just lint identity-literals`

`just build` runs generation, the fast lint gate, and a workspace build with all features.

`just test all` is the strict end-to-end local verification path. It cleans the repo, regenerates code, runs version checks, runs the selected lint suite, and executes the Rust workspace tests with all features.

## Tooling notes

- Rust lint/build checks are wired through `sc-lint` where practical.
- The boundary analyzer is exposed as `just lint sc-boundary`.
- The string-duplication / canonical literal lint is exposed as `just lint identity-literals`.
- Code generation currently depends on Python packages used by the legacy generator.

## Current status

This repo is in transition. The old reference crates build and test locally from the new root workspace, but the new `units-x` crate/package surfaces are still in the planning and bootstrap phase.
