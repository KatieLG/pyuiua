//! Uiua runtime wrapper for Python

use pyo3::exceptions::PyRuntimeError;
use pyo3::types::PyList;
use pyo3::{create_exception, prelude::*};
use uiua::Uiua;

use crate::convert::{pyobject_to_uiua_value, uiua_value_to_pyobject};

#[pyclass(name = "Uiua")]
pub struct PyUiua {
    uiua: Uiua,
}

create_exception!(pyuiua, UiuaError, PyRuntimeError);

// Convert any errors to a python UiuaError
fn to_uiua_error(e: impl std::fmt::Display) -> PyErr {
    UiuaError::new_err(e.to_string())
}

#[pymethods]
impl PyUiua {
    /// Create a new Uiua instance
    #[new]
    fn new() -> Self {
        PyUiua {
            uiua: Uiua::with_native_sys(),
        }
    }

    /// Push a Python value onto the stack
    fn push<'py>(&mut self, py: Python<'py>, value: &Bound<'py, PyAny>) -> PyResult<()> {
        let uiua_value = pyobject_to_uiua_value(py, value, &self.uiua)?;
        self.uiua.push(uiua_value);
        Ok(())
    }

    /// Pop a value from the stack and convert to Python
    fn pop<'py>(&mut self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let value = self.uiua.pop(1).map_err(to_uiua_error)?;
        uiua_value_to_pyobject(py, &value)
    }

    /// Get all values from the stack without removing them
    fn stack<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let py_values: PyResult<Vec<_>> = self
            .uiua
            .stack()
            .iter()
            .map(|v| uiua_value_to_pyobject(py, v))
            .collect();

        PyList::new(py, py_values?)
    }

    /// Run Uiua code on the current stack
    fn run(&mut self, code: &str) -> PyResult<()> {
        self.uiua.run_str(code).map(|_| ()).map_err(to_uiua_error)
    }

    /// Clear the stack
    fn clear(&mut self) {
        self.uiua.take_stack();
    }

    /// Return number of values on stack
    fn __len__(&self) -> usize {
        self.uiua.stack().len()
    }

    /// String representation
    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        if self.uiua.stack().is_empty() {
            return Ok("Uiua(stack=[])".to_string());
        }

        let stack_reprs: PyResult<Vec<_>> = self
            .uiua
            .stack()
            .iter()
            .map(|v| {
                let py_val = uiua_value_to_pyobject(py, v)?;
                Ok(py_val.repr()?.to_string())
            })
            .collect();

        Ok(format!("Uiua(stack=[{}])", stack_reprs?.join(", ")))
    }
}
