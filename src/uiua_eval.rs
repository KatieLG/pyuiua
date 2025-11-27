//! Standalone eval function for Uiua

use pyo3::prelude::*;
use pyo3::types::PyTuple;
use uiua::Uiua;

use crate::convert::{pyobject_to_uiua_value, uiua_value_to_pyobject};
use crate::uiua_runtime::to_uiua_error;

/// Run Uiua code with optional inputs and return the resulting value(s).
#[pyfunction]
#[pyo3(signature = (code, *args))]
pub fn eval<'py>(
    py: Python<'py>,
    code: &str,
    args: &Bound<'py, PyTuple>,
) -> PyResult<Bound<'py, PyAny>> {
    let mut uiua = Uiua::with_native_sys();

    // Push in reverse order to align with Uiua's right to left arg consumption
    for arg in args.iter().rev() {
        let uiua_value = pyobject_to_uiua_value(py, &arg, &uiua)?;
        uiua.push(uiua_value);
    }

    uiua.run_str(code).map_err(to_uiua_error)?;

    let stack = uiua.take_stack();
    match stack.len() {
        0 => Ok(py.None().into_bound(py)),
        1 => uiua_value_to_pyobject(py, &stack[0]),
        _ => {
            let py_values: PyResult<Vec<_>> = stack
                .iter()
                .rev()
                .map(|v| uiua_value_to_pyobject(py, v))
                .collect();
            Ok(PyTuple::new(py, py_values?)?.into_any())
        }
    }
}
