//! Python bindings for the Uiua programming language.

use pyo3::prelude::*;

mod convert;
mod uiua_runtime;

use uiua_runtime::PyUiua;

#[pymodule]
fn pyuiua(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyUiua>()?;
    Ok(())
}
