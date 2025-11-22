use pyo3::prelude::*;
use pyo3::types::PyList;
use uiua::{Uiua, Value};

/// Convert a Uiua Value to a Python object
fn value_to_pyobject<'py>(py: Python<'py>, value: Value, uiua: &Uiua) -> PyResult<Bound<'py, PyAny>> {

    // check if scalar
    if value.shape.is_empty(){ 
        // Try as int
        if let Ok(i) = value.as_int(uiua, "") {
            return Ok(i.into_pyobject(py)?.into_any());
        }

        // Try as float
        if let Ok(n) = value.as_num(uiua, "") {
            return Ok(n.into_pyobject(py)?.into_any());
        }

        // Try as string
        if let Ok(s) = value.as_string(uiua, "") {
            return Ok(s.into_pyobject(py)?.into_any());
        }

        // Try as bytes
        if let Ok(bytes) = value.as_bytes(uiua, "") {
            let bytes_vec: Vec<u8> = bytes.into_owned();
            return Ok(bytes_vec.into_pyobject(py)?.into_any());
        }

        // otherwise return None
        return Ok(py.None().into_bound(py).into_any())
    }

    // if not scalar - return a list
    return array_to_pylist(py, &value, uiua)
}

/// Convert a Uiua Array to a nested Python list
fn array_to_pylist<'py>(py: Python<'py>, value: &Value, uiua: &Uiua) -> PyResult<Bound<'py, PyAny>> {

    // Check if this is a string (character array)
    if let Ok(s) = value.as_string(uiua, "") {
        return Ok(s.into_pyobject(py)?.into_any());
    }

    // for box arrays unbox each element
    if value.as_box_array().is_some() {
        let len = value.shape[0];
        let list = PyList::empty(py);

        for i in 0..len {
            let mut v = value.row(i);
            // Unbox the element
            while v.as_box().is_some() {
                v = v.unboxed();
            }
            let py_val = value_to_pyobject(py, v, uiua)?;
            list.append(py_val)?;
        }

        return Ok(list.into_any());
    }

    // otherwise convert each list element

    let len = value.shape[0];
    let list = PyList::empty(py);

    for i in 0..len {
        let v = value.row(i);
        let py_val = value_to_pyobject(py, v, uiua)?;
        list.append(py_val)?;
    }

    Ok(list.into_any())
}

/// Execute Uiua code and return the top value from the stack
///
/// # Arguments
/// * `code` - Uiua code to execute
///
/// # Returns
/// The top value from the Uiua stack, converted to a Python object
#[pyfunction]
fn uiua_eval<'py>(py: Python<'py>, code: &str) -> PyResult<Bound<'py, PyAny>> {
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

/// Create the pyuiua module
#[pymodule]
fn pyuiua(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(uiua_eval, m)?)?;
    Ok(())
}
