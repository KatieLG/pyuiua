//! Python bindings for the Uiua programming language.

use pyo3::prelude::*;

mod convert;
mod uiua_runtime;

use uiua_runtime::PyUiua;

#[pymodule]
fn pyuiua(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyUiua>()?;
    m.add("UiuaError", m.py().get_type::<uiua_runtime::UiuaError>())?;
    m.add("UiuaValue", m.py().get_type::<pyo3::types::PyAny>())?;
    Ok(())
}
