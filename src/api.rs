//! Python API functions for executing Uiua code

use pyo3::prelude::*;
use pyo3::types::PyList;
use uiua::Uiua;

use crate::convert::value_to_pyobject;

/// Execute Uiua code and return the top value from the stack
///
/// # Arguments
/// * `code` - Uiua code to execute
///
/// # Returns
/// The top value from the Uiua stack, converted to a Python object
#[pyfunction]
pub fn uiua_eval<'py>(py: Python<'py>, code: &str) -> PyResult<Bound<'py, PyAny>> {
    let mut uiua = Uiua::with_native_sys();

    uiua.run_str(code)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            format!("Uiua error: {}", e)
        ))?;

    let mut stack = uiua.take_stack();

    if stack.is_empty() {
        Ok(py.None().into_bound(py).into_any())
    } else {
        value_to_pyobject(py, stack.pop().unwrap(), &uiua)
    }
}

/// Execute Uiua code and return the entire stack as a list
///
/// # Arguments
/// * `code` - Uiua code to execute
///
/// # Returns
/// A list containing all values from the Uiua stack converted to Python objects
#[pyfunction]
pub fn uiua_stack<'py>(py: Python<'py>, code: &str) -> PyResult<Bound<'py, PyAny>> {
    let mut uiua = Uiua::with_native_sys();

    uiua.run_str(code)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            format!("Uiua error: {}", e)
        ))?;

    let stack = uiua.take_stack();

    // Convert all stack values to Python objects
    let list = PyList::empty(py);

    for value in stack {
        let py_val = value_to_pyobject(py, value, &uiua)?;
        list.append(py_val)?;
    }

    Ok(list.into_any())
}
