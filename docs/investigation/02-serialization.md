# Serialization Investigation

## What exists today

The repository has one structured serialization path:

- Optional `serde` support via the `serde` dependency in [simple-si-units/Cargo.toml](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/Cargo.toml:24)

Each unit struct conditionally derives `Serialize` and `Deserialize`, for example:

- [Amount<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:24)
- [Distance<T>](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2037)
- Equivalent derives appear throughout the other unit modules

The README accurately advertises serde as an optional feature in [README.md](/Volumes/Extreme%20Pro/github/simple-si-units/README.md:55).

## What that means concretely

The crate does not implement format-specific serializers itself. Instead, it implements the serde traits so that downstream code can use any serde-compatible format crate.

Examples of formats a downstream user could choose:

- JSON via `serde_json`
- CBOR via `serde_cbor`
- bincode
- postcard
- YAML
- TOML

These are not bundled in this repository.

## Expected wire shape

Because the derives are attached to named-field structs, the natural serde representation is a map/object with the field name as the key.

Representative example:

- `Distance<f64>` is declared as `pub struct Distance<T: NumLike> { pub m: T }` in [simple-si-units/src/base.rs](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:2039)
- With serde enabled, a JSON serializer would therefore be expected to produce a shape like `{\"m\": 1.23}`

Similarly:

- `Amount<f64>` would serialize like `{\"mol\": ...}`
- `Velocity<f64>` would serialize like `{\"mps\": ...}`

This is an inference from standard serde derive behavior on named-field structs.

## Other serialization-adjacent surfaces

The crate also provides:

- `fmt::Display` for human-readable formatting, for example [Amount display impl](/Volumes/Extreme%20Pro/github/simple-si-units/reference/simple-si-units/src/base.rs:58)
- Public fields and `to_*` methods for manual extraction

These are useful for ad hoc persistence, but they are not formal structured-serialization APIs.

## Gaps

### No built-in format wrappers

There is no repository-owned helper API such as:

- `to_json()`
- `from_json()`
- `to_bytes()`
- `from_bytes()`

### No wire-compatibility policy

There is no documented stability promise for field names or serialization shape. That matters because the field names are part of the serialized form.

### No serialization tests

I did not find tests exercising serde round trips or pinning a serialized representation. That means accidental field renames could silently change the wire format.

## Recommendation

If serialized form matters externally, add:

1. A small serde round-trip test suite
2. At least one snapshot or exact-shape test for representative types
3. A documented policy on whether field names are stable API
