//! Primary Rust deliverable crate for the `units-x` project.
//!
//! Phase A provides scaffolding only. The quantity model, catalog-driven
//! generation, serialization, and interop surfaces land in later phases.

use pyo3::prelude::*;

/// Current package version exposed for scaffolding and smoke-test use.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

#[pyfunction]
fn version() -> &'static str {
    VERSION
}

#[pymodule]
fn _native(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add("__version__", VERSION)?;
    module.add_function(wrap_pyfunction!(version, module)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::{version, VERSION};

    #[test]
    fn version_constant_is_wired() {
        assert_eq!(VERSION, env!("CARGO_PKG_VERSION"));
    }

    #[test]
    fn python_version_function_is_wired() {
        assert_eq!(version(), env!("CARGO_PKG_VERSION"));
    }
}
