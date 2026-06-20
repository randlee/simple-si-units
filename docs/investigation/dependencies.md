# Dependency Inventory

## Sources

- [simple-si-units/Cargo.toml](</Volumes/Extreme Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:17>)
- [simple-si-units-core/Cargo.toml](</Volumes/Extreme Pro/github/simple-si-units/reference/simple-si-units-core/Cargo.toml:17>)
- [simple-si-units-macros/Cargo.toml](</Volumes/Extreme Pro/github/simple-si-units/reference/simple-si-units-macros/Cargo.toml:19>)

## simple-si-units

Manifest: [simple-si-units/Cargo.toml](</Volumes/Extreme Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:17>)

Normal dependencies:

- `simple-si-units-macros = "1.0.1"`: internal crate name, but declared as a registry version dependency; a local `reference/` `path` form is present only as a commented-out alternative in the manifest.
- `simple-si-units-core = "1.0.1"`: internal crate name, but declared as a registry version dependency; a local `reference/` `path` form is present only as a commented-out alternative in the manifest.

Optional dependencies:

- `serde = { version = "1.0", optional = true, features = ["derive"] }`
- `uom = { version = "0.34", optional = true, features = ["si", "f64"] }`
- `num-complex = { version = "0.4", optional = true }`
- `num-bigfloat = { version = "1.6", optional = true }`

Dev dependencies:

- `serde = { version = "1.0", features = ["derive"] }`
- `num-complex = "0.4"`
- `num-bigfloat = "1.6"`
- `num-traits = "0.2"`
- `num = "0.4"`
- `uom = "0.34"`

Other manifest notes:

- [build-dependencies] exists in [simple-si-units/Cargo.toml](</Volumes/Extreme Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:38>) but is explicitly empty.
- Current Cargo resolution from this crate uses registry sources for `simple-si-units-core` and `simple-si-units-macros`; the local `reference/` crate directories are not active unless the commented `path` entries are restored.

## simple-si-units-core

Manifest: [simple-si-units-core/Cargo.toml](</Volumes/Extreme Pro/github/simple-si-units/reference/simple-si-units-core/Cargo.toml:17>)

Normal dependencies:

- None.

Optional dependencies:

- None.

Dev dependencies:

- None.

Other manifest notes:

- The crate has no declared outbound dependencies at all in its manifest.

## simple-si-units-macros

Manifest: [simple-si-units-macros/Cargo.toml](</Volumes/Extreme Pro/github/simple-si-units/reference/simple-si-units-macros/Cargo.toml:19>)

Normal dependencies:

- `simple-si-units-core = "1.0"`: internal crate name, but declared as a registry version dependency; a local `reference/` `path` form is present only as a commented-out alternative in the manifest.
- `syn = { version = "1.0", features = ["full", "extra-traits"] }`
- `quote = "1.0"`

Optional dependencies:

- None.

Dev dependencies:

- `proc-macro2 = "1.0"`
- `macrotest = "1.0"`

Other manifest notes:

- Current Cargo resolution from this crate uses the registry source for `simple-si-units-core`; the local `reference/` crate directory is not active unless the commented `path` entry is restored.

## Internal vs. Registry Wiring Summary

Internal crate dependency edges declared in this repo:

- `simple-si-units -> simple-si-units-macros`
- `simple-si-units -> simple-si-units-core`
- `simple-si-units-macros -> simple-si-units-core`

For each of those edges, the active manifest entry is a versioned registry dependency, not a local `path` dependency. The manifests preserve commented-out `path = "../..."` alternatives, which document how the crates could be rewired to use the local `reference/` directories instead.
