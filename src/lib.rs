use pyo3::prelude::*;
use uiua::*;

/// uiua eval input.
#[pyfunction]
fn uiua_eval(code: &str) -> PyResult<Vec<String>> {
    let mut uiua = Uiua::with_native_sys();
    uiua.run_str(code).unwrap();
    let stack = uiua.take_stack().into_iter().map(|v| v.to_string()).collect();
    Ok(stack)
}

/// Create the pyuiua module.
#[pymodule]
fn pyuiua(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(uiua_eval, m)?)?;
    Ok(())
}
