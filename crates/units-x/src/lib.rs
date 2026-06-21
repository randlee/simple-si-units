//! Primary Rust deliverable crate for the `units-x` project.
//!
//! Phase A provides scaffolding only. The quantity model, catalog-driven
//! generation, serialization, and interop surfaces land in later phases.

/// Current package version exposed for scaffolding and smoke-test use.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

#[cfg(test)]
mod tests {
    use super::VERSION;

    #[test]
    fn version_constant_is_wired() {
        assert_eq!(VERSION, env!("CARGO_PKG_VERSION"));
    }
}
