//! Python binding scaffold for the `units-x` project.
//!
//! This crate owns the PyO3 boundary so the primary `units-x` crate can remain
//! a Rust-first library surface.

use pyo3::prelude::*;
use units_x::VERSION;

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
    use super::version;
    use units_x::VERSION;

    #[test]
    fn python_version_function_is_wired() {
        assert_eq!(version(), VERSION);
    }
}
