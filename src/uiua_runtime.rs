//! Uiua runtime wrapper for Python

use pyo3::prelude::*;
use pyo3::types::PyList;
use uiua::Uiua;

use crate::convert::{pyobject_to_value, value_to_pyobject};

/// A Uiua instance with a stack
#[pyclass(name = "Uiua")]
pub struct PyUiua {
    uiua: Uiua,
}

#[pymethods]
impl PyUiua {
    /// Create a new Uiua runtime instance
    #[new]
    fn new() -> Self {
        PyUiua {
            uiua: Uiua::with_native_sys(),
        }
    }

    /// Push a Python value onto the stack
    fn push<'py>(&mut self, py: Python<'py>, value: &Bound<'py, PyAny>) -> PyResult<()> {
        let uiua_value = pyobject_to_value(py, value, &self.uiua)?;
        self.uiua.push(uiua_value);
        Ok(())
    }

    /// Pop a value from the stack and convert to Python
    fn pop<'py>(&mut self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let value = self.uiua.pop("No values on stack").map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!(
                "Failed to pop from stack: {}",
                e
            ))
        })?;

        // Create a temporary uiua instance for conversion
        let temp_uiua = Uiua::with_native_sys();
        value_to_pyobject(py, value, &temp_uiua)
    }

    /// Get all values from the stack without removing them
    fn stack<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let stack = self.uiua.stack();
        let list = PyList::empty(py);

        let temp_uiua = Uiua::with_native_sys();
        // Reverse the iteration so top of stack is at the end of list
        let values: Vec<_> = stack.iter().cloned().collect();
        for value in values.iter().rev() {
            let py_val = value_to_pyobject(py, (*value).clone(), &temp_uiua)?;
            list.append(py_val)?;
        }

        Ok(list.into_any())
    }

    /// Run Uiua code on the current stack
    fn run(&mut self, code: &str) -> PyResult<()> {
        self.uiua.run_str(code).map(|_| ()).map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Uiua error: {}", e))
        })
    }

    /// Clear the stack
    fn clear(&mut self) {
        self.uiua.take_stack();
    }

    /// Get the number of values on the stack
    fn __len__(&self) -> usize {
        self.uiua.stack().len()
    }

    /// String representation
    fn __repr__(&self) -> String {
        let stack = self.uiua.stack();
        if stack.is_empty() {
            return "Uiua(stack=[])".to_string();
        }

        // Format stack values using Uiua's Display implementation
        let stack_repr: Vec<String> = stack.iter().map(|v| format!("{}", v)).collect();

        format!("Uiua(stack=[{}])", stack_repr.join(", "))
    }
}
