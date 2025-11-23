//! Python to Uiua conversions

use pyo3::prelude::*;
use pyo3::types::{PyFloat, PyInt, PyList, PyString};
use uiua::{Uiua, Value};

/// Convert Python object to Uiua Value
pub fn pyobject_to_uiua_value(
    py: Python<'_>,
    obj: &Bound<'_, PyAny>,
    uiua: &Uiua,
) -> PyResult<Value> {
    // Try int
    if let Ok(i) = obj.extract::<i64>() {
        // Uiua uses f64 so precision loss expected for large ints
        #[allow(clippy::cast_precision_loss)]
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
        return pylist_to_uiua_value(py, list, uiua);
    }

    Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
        "Cannot convert type {} to Uiua value",
        obj.get_type().name()?
    )))
}

/// Convert Python list to Uiua Value
fn pylist_to_uiua_value(py: Python<'_>, list: &Bound<'_, PyList>, uiua: &Uiua) -> PyResult<Value> {
    let len = list.len();

    if len == 0 {
        return Ok(Value::from_row_values_infallible(Vec::<Value>::new()));
    }

    let first = list.get_item(0)?;

    // Try to convert to a numeric array
    if first.is_instance_of::<PyInt>() || first.is_instance_of::<PyFloat>() {
        if let Ok(nums) = list
            .iter()
            .map(|item| item.extract::<f64>())
            .collect::<PyResult<Vec<_>>>()
        {
            let values: Vec<Value> = nums.into_iter().map(Value::from).collect();
            return Ok(Value::from_row_values_infallible(values));
        }
    }
    // Try to convert to a string array
    else if first.is_instance_of::<PyString>()
        && let Ok(strings) = list
            .iter()
            .map(|item| item.extract::<String>())
            .collect::<PyResult<Vec<_>>>()
    {
        let char_arrays: Vec<Value> = strings.iter().map(|s| Value::from(s.as_str())).collect();
        if let Ok(value) = Value::from_row_values(char_arrays, uiua) {
            return Ok(value);
        }
    }

    // Fallback to a boxed array
    pylist_to_boxed_uiua_value(py, list, uiua)
}

/// Convert Python list to boxed Uiua array
fn pylist_to_boxed_uiua_value(
    py: Python<'_>,
    list: &Bound<'_, PyList>,
    uiua: &Uiua,
) -> PyResult<Value> {
    let mut values = Vec::new();

    for item in list.iter() {
        let mut val = pyobject_to_uiua_value(py, &item, uiua)?;
        val.box_it();
        values.push(val);
    }

    Value::from_row_values(values, uiua).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
            "Failed to create boxed array: {e}"
        ))
    })
}
