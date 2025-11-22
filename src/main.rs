use pyo3::prelude::*;
use uiua::*;

#[derive(Debug)]
pub enum PyValue {
    Byte(Vec<u8>),
    Num(Vec<f64>),
    Complex(Vec<Complex>),
    Char(Vec<char>),
    Box(Vec<Boxed>),
}

#[derive(Debug)]
pub enum Complex {
    Real(f64),
    Imaginary(f64),
}

#[derive(Debug)]
pub enum Boxed {
    SomeValue,
}
// Function to convert the stack to a vector of either numbers or strings
fn convert_stack(stack: Vec<Value>) -> Vec<String> {
    stack.into_iter().map(|value| {
        match value {
            Value::Num(arr) => arr.to_string(),
            _ => value.to_string(),
        }
    }).collect()
}

// Example main function to demonstrate usage
fn main() {
    // Example of a Vec<Value>
    let mut uiua = Uiua::with_native_sys();
    uiua.run_str("fix.fix.1").unwrap();
    let stack = uiua.take_stack();

    // Convert the stack
    let result = convert_stack(stack);
    println!("Result: {:?}", result);
}
