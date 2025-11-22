//! Python to Uiua conversions

use pyo3::prelude::*;
use pyo3::types::{PyFloat, PyInt, PyList, PyString};
use uiua::{Uiua, Value};

/// Convert Python object to Uiua Value
pub fn pyobject_to_value(py: Python<'_>, obj: &Bound<'_, PyAny>, uiua: &Uiua) -> PyResult<Value> {
    // Try int
    if let Ok(i) = obj.extract::<i64>() {
        return Ok(Value::from(i as f64));
    }

    // Try float
    if let Ok(f) = obj.extract::<f64>() {
        return Ok(Value::from(f));
    }

    // Try string
    if let Ok(s) = obj.extract::<String>() {
        return Ok(Value::from(s.as_str()));
    }

    // Try list
    if let Ok(list) = obj.cast::<PyList>() {
        return pylist_to_value(py, list, uiua);
    }

    Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
        "Cannot convert type {} to Uiua value",
        obj.get_type().name()?
    )))
}

/// Convert Python list to Uiua Value
fn pylist_to_value(py: Python<'_>, list: &Bound<'_, PyList>, uiua: &Uiua) -> PyResult<Value> {
    let len = list.len();

    if len == 0 {
        return Ok(Value::from_row_values_infallible(Vec::<Value>::new()));
    }

    let first = list.get_item(0)?;

    // Try to convert as numeric array
    if first.is_instance_of::<PyInt>() || first.is_instance_of::<PyFloat>() {
        let mut values = Vec::with_capacity(len);
        for item in list.iter() {
            if let Ok(n) = item.extract::<f64>() {
                values.push(Value::from(n));
            } else {
                // Mixed types - return boxed array
                return pylist_to_boxed(py, list, uiua);
            }
        }
        return Ok(Value::from_row_values_infallible(values));
    }

    // Try to convert as string array
    if first.is_instance_of::<PyString>() {
        let strings: Vec<String> = list
            .iter()
            .map(|item| {
                if let Ok(s) = item.extract::<String>() {
                    Ok(s)
                } else {
                    Ok(String::new())
                }
            })
            .collect::<PyResult<_>>()?;

        let char_arrays: Vec<Value> = strings.iter().map(|s| Value::from(s.as_str())).collect();

        if let Ok(array) = Value::from_row_values(char_arrays, uiua) {
            return Ok(array);
        }
    }

    // Mixed types or nested lists - create boxed array
    pylist_to_boxed(py, list, uiua)
}

/// Convert Python list to boxed Uiua array
fn pylist_to_boxed(py: Python<'_>, list: &Bound<'_, PyList>, uiua: &Uiua) -> PyResult<Value> {
    let mut values = Vec::new();

    for item in list.iter() {
        let mut val = pyobject_to_value(py, &item, uiua)?;
        val.box_it();
        values.push(val);
    }

    Value::from_row_values(values, &mut uiua::Uiua::with_native_sys()).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
            "Failed to create boxed array: {}",
            e
        ))
    })
}
