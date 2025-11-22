//! Python bindings for Uiua

use pyo3::prelude::*;

mod api;
mod convert;

use api::{uiua_eval, uiua_stack};

/// Create the pyuiua module
#[pymodule]
fn pyuiua(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(uiua_eval, m)?)?;
    m.add_function(wrap_pyfunction!(uiua_stack, m)?)?;
    Ok(())
}
