# python-uiua

A Python binding for [Uiua](https://www.uiua.org/), a stack-based array programming language written in Rust. 
This package allows executing Uiua directly from Python.

## Requirements

- Python 3.10 or higher

## Installation

```bash
pip install pyuiua
```

## Example Usage

```python
import pyuiua

# Create a Uiua instance
uiua = pyuiua.Uiua()

# Basic evaluation - run code and pop result
uiua.run("/×⇡₁10") # Calculate 10 factorial
print(uiua.pop())  # 3628800

# Push Python values onto the stack
uiua.push(10)
uiua.push(20)
uiua.run("+") # Then run a Uiua operation
print(uiua.pop())  # 30

# Work with arrays
uiua.push([1, 2, 3, 4, 5])
uiua.run("/+")  # Sum the array
print(uiua.pop())  # 15

# Inspect the stack without modifying it
uiua.push(1)
uiua.push(2)
uiua.push(3)
print(uiua.stack())  # [3, 2, 1]
print(len(uiua))     # 3

# Clear the stack
uiua.clear()
```

See `example/run_uiua.py` for more examples.

## API Reference

**`Uiua()`** - Create a Uiua instance
- `uiua.push(value)` - Push a Python value onto the stack
- `uiua.pop()` - Pop a value from the stack and convert to Python
- `uiua.run(code)` - Execute Uiua code on the current stack
- `uiua.stack()` - Inspect the stack without modifying it
- `uiua.clear()` - Remove all values from the stack
- `len(uiua)` - Get the number of values on the stack

## Type Conversions

The conversion of types is currently lossy. Both arrays and boxes convert to lists in Python, and Python lists convert 
to an array if they're homogeneous with a well-defined shape, otherwise a box. As a result, a box in Uiua of homogeneous
values will become an array when converted to python and back.

### Uiua → Python

| Uiua Type                    | Python Type      |
|------------------------------|------------------|
| Scalar number                | `int` or `float` |
| Scalar char                  | `str`            |
| Scalar byte                  | `int`            |
| 1D Array                     | `list`           |
| Multi-dimensional Array      | Nested `list`    |
| Box Array (heterogeneous)    | `list`           |

### Python → Uiua

| Python Type          | Uiua Type              |
|----------------------|------------------------|
| `int`                | Scalar number          |
| `float`              | Scalar number          |
| `str`                | Character array/string |
| `list` (single type) | Array                  |
| `list` (mixed)       | Box Array              |

## Development

### Requirements

- Python 3.10 or higher
- Rust 1.83.0 or higher

### Set-up

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/python-uiua.git
   cd python-uiua
   ```

2. Install maturin:
   ```bash
   uv tool install maturin
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Build and install:
   ```bash
   maturin develop
   ```

## Links

- [Uiua Language](https://www.uiua.org/)
- [PyO3 Documentation](https://pyo3.rs/)
- [Maturin Documentation](https://www.maturin.rs/)
