//! Python bindings for Uiua

use pyo3::prelude::*;

mod convert;
mod uiua_runtime;

use uiua_runtime::PyUiua;

/// Create the pyuiua module
#[pymodule]
fn pyuiua(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyUiua>()?;
    Ok(())
}
