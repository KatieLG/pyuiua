use pyo3::prelude::*;
use pyo3::types::PyList;
use uiua::{Uiua, Value};

/// Convert a Uiua Value to a Python object
pub fn value_to_pyobject<'py>(py: Python<'py>, value: Value, uiua: &Uiua) -> PyResult<Bound<'py, PyAny>> {

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

