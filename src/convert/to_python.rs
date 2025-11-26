//! Uiua to Python conversions

use pyo3::prelude::*;
use pyo3::types::PyList;
use uiua::{Uiua, Value};

/// Convert Uiua value to Python object
pub fn uiua_value_to_pyobject<'py>(
    py: Python<'py>,
    value: &Value,
    uiua: &Uiua,
) -> PyResult<Bound<'py, PyAny>> {
    if value.shape.is_empty() {
        return uiua_scalar_to_pyobject(py, value, uiua);
    }

    if let Ok(s) = value.as_string(uiua, "") {
        return Ok(s.into_pyobject(py)?.into_any());
    }

    uiua_array_to_pylist(py, value, uiua).map(pyo3::Bound::into_any)
}

/// Convert a Uiua array to a Python list
fn uiua_array_to_pylist<'py>(
    py: Python<'py>,
    value: &Value,
    uiua: &Uiua,
) -> PyResult<Bound<'py, PyList>> {
    let is_boxed = value.as_box_array().is_some();
    let len = value.shape[0];
    let list = PyList::empty(py);

    for i in 0..len {
        let mut v = value.row(i);
        // If this is a boxed array, unbox the elements
        while is_boxed && v.as_box().is_some() {
            v = v.unboxed();
        }
        let py_val = uiua_value_to_pyobject(py, &v, uiua)?;
        list.append(py_val)?;
    }

    Ok(list)
}

/// Convert Uiua scalar to a Python scalar
fn uiua_scalar_to_pyobject<'py>(
    py: Python<'py>,
    value: &Value,
    uiua: &Uiua,
) -> PyResult<Bound<'py, PyAny>> {
    // Helper to convert to PyAny
    macro_rules! try_convert {
        ($expr:expr) => {
            if let Ok(val) = $expr {
                return Ok(val.into_pyobject(py)?.into_any());
            }
        };
    }

    try_convert!(value.as_int(uiua, ""));
    try_convert!(value.as_num(uiua, ""));
    try_convert!(value.as_string(uiua, ""));

    if let Some(boxed) = value.as_box() {
        return uiua_value_to_pyobject(py, &boxed.0, uiua);
    }

    // If all conversions fail, raise a Type Error
    Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
        "Error converting Uiua type {} to a Python type",
        value.type_name()
    )))
}
