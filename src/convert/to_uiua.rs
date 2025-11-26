//! Python to Uiua conversions

use pyo3::prelude::*;
use pyo3::types::{PyComplex, PyFloat, PyInt, PyList, PyString};
use uiua::{Complex, Uiua, Value};

/// Convert Python object to Uiua Value
pub fn pyobject_to_uiua_value(
    py: Python<'_>,
    obj: &Bound<'_, PyAny>,
    uiua: &Uiua,
) -> PyResult<Value> {
    if obj.is_instance_of::<PyInt>() {
        if let Ok(n) = obj.extract::<u8>() {
            return Ok(Value::from(n));
        }
        return Ok(Value::from(obj.extract::<f64>()?));
    }
    if obj.is_instance_of::<PyFloat>() {
        return Ok(Value::from(obj.extract::<f64>()?));
    }
    if obj.is_instance_of::<PyComplex>() {
        let c = obj.cast::<PyComplex>()?;
        return Ok(Value::from(Complex::new(c.real(), c.imag())));
    }
    if obj.is_instance_of::<PyString>() {
        return Ok(Value::from(obj.extract::<&str>()?));
    }
    if obj.is_instance_of::<PyList>() {
        return pylist_to_uiua_value(py, obj.cast::<PyList>()?, uiua);
    }

    Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(format!(
        "Cannot convert type {} to Uiua value",
        obj.get_type().name()?
    )))
}

/// Convert Python list to Uiua Value
fn pylist_to_uiua_value(py: Python<'_>, list: &Bound<'_, PyList>, uiua: &Uiua) -> PyResult<Value> {
    if list.is_empty() {
        return Ok(Value::from_row_values_infallible(Vec::<Value>::new()));
    }

    let first = list.get_item(0)?;

    // Try int array
    if first.is_instance_of::<PyInt>()
        && let Ok(bytes) = list
            .iter()
            .map(|item| item.extract::<u8>())
            .collect::<PyResult<Vec<_>>>()
    {
        let values: Vec<Value> = bytes.into_iter().map(Value::from).collect();
        return Ok(Value::from_row_values_infallible(values));
    }

    // Try float array
    if (first.is_instance_of::<PyInt>() || first.is_instance_of::<PyFloat>())
        && let Ok(nums) = list
            .iter()
            .map(|item| item.extract::<f64>())
            .collect::<PyResult<Vec<_>>>()
    {
        let values: Vec<Value> = nums.into_iter().map(Value::from).collect();
        return Ok(Value::from_row_values_infallible(values));
    }

    // Try string array
    if first.is_instance_of::<PyString>()
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

    // Fallback to boxed array
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
