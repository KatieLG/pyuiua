//! Uiua to Python conversions

use pyo3::prelude::*;
use pyo3::types::{PyComplex, PyList};
use uiua::Value;

/// Convert Uiua value to Python object
pub fn uiua_value_to_pyobject<'py>(py: Python<'py>, value: &Value) -> PyResult<Bound<'py, PyAny>> {
    let is_scalar = value.shape.is_empty();

    macro_rules! convert {
        ($arr:expr) => {
            if is_scalar {
                Ok($arr
                    .elements()
                    .next()
                    .unwrap()
                    .into_pyobject(py)?
                    .into_any())
            } else {
                array_to_pylist(py, value)
            }
        };
        ($arr:expr, $scalar:expr) => {
            if is_scalar {
                $scalar
            } else {
                array_to_pylist(py, value)
            }
        };
    }

    match value {
        Value::Num(arr) => convert!(arr),
        Value::Byte(arr) => convert!(arr),
        Value::Char(arr) => {
            if value.shape.len() == 1 {
                Ok(arr
                    .elements()
                    .collect::<String>()
                    .into_pyobject(py)?
                    .into_any())
            } else {
                convert!(arr)
            }
        }
        Value::Complex(arr) => convert!(arr, {
            let c = arr.elements().next().unwrap();
            Ok(PyComplex::from_doubles(py, c.re, c.im).into_any())
        }),
        Value::Box(arr) => convert!(arr, {
            uiua_value_to_pyobject(py, &arr.elements().next().unwrap().0)
        }),
    }
}

/// Convert a Uiua array to a Python list
fn array_to_pylist<'py>(py: Python<'py>, value: &Value) -> PyResult<Bound<'py, PyAny>> {
    let items: PyResult<Vec<_>> = value
        .rows()
        .map(|row| uiua_value_to_pyobject(py, &row))
        .collect();
    Ok(PyList::new(py, items?)?.into_any())
}
