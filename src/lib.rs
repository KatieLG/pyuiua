//! Python bindings for the Uiua programming language.

use pyo3::prelude::*;

mod convert;
mod uiua_eval;
mod uiua_runtime;

use uiua_eval::eval;
use uiua_runtime::{PyUiua, UiuaError};

#[pymodule]
fn pyuiua(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyUiua>()?;
    m.add("UiuaError", m.py().get_type::<UiuaError>())?;
    m.add("UiuaValue", m.py().get_type::<pyo3::types::PyAny>())?;
    m.add_function(wrap_pyfunction!(eval, m)?)?;
    Ok(())
}
