# PyUiua

A Python binding for [Uiua](https://www.uiua.org/), allowing interaction between Uiua and Python.

## Requirements

- Python 3.10 or higher

## Installation

```bash
pip install pyuiua
```

or see dev setup below for building from source

## Example Usage

### Eval method

```python
import pyuiua

pyuiua.eval("+ 1 2")           # 3
pyuiua.eval("/+", [1, 2, 3])   # 6
pyuiua.eval("/×⇡₁10")          # 3628800 (10 factorial)
pyuiua.eval("∩+", 1, 2, 3, 4)  # (3, 7)
```

### Persisted instance

```python
import pyuiua

uiua = pyuiua.Uiua()

# Push Python values onto the stack and operate on them
uiua.push(10)
uiua.push(20)
uiua.run("+")
print(uiua.pop())  # 30

# Work with arrays
uiua.push([1, 2, 3, 4, 5])
uiua.run("/+")
print(uiua.pop())  # 15

# Inspect the stack
uiua.push(1)
uiua.push(2)
uiua.push(3)
print(uiua.stack())  # [1, 2, 3]
print(len(uiua))     # 3

# Clear the stack
uiua.clear()
```

## API Reference

**`pyuiua.eval(code, *args)`** - Run Uiua code with any number of inputs and return the resulting value or tuple or values (or None if no output)

**`pyuiua.Uiua()`** - Create a Uiua instance

- `uiua.push(value)` - Push a Python value onto the stack
- `uiua.pop()` - Pop a value from the stack and return it
- `uiua.run(code)` - Execute Uiua code on the current stack
- `uiua.stack()` - Return all stack values as a list (without modifying)
- `uiua.clear()` - Remove all values from the stack
- `len(uiua)` - Get the number of values on the stack

## Type Conversions

The conversion of types is currently lossy. Both arrays and boxes convert to lists in Python, and Python lists convert
to an array if they're homogeneous with a well-defined shape, otherwise a box. As a result, a box in Uiua of homogeneous
values will become an array when converted to python and back.

- **Currently supports**: most scalars, multidimensional arrays, and boxed arrays
- **Does not yet support**: maps, functions, or user-defined types

### Uiua → Python

| Uiua Type                 | Python Type      |
| ------------------------- | ---------------- |
| Scalar number             | `int` or `float` |
| Scalar char               | `str`            |
| Scalar byte               | `int`            |
| 1D Array                  | `list`           |
| Multi-dimensional Array   | Nested `list`    |
| Box Array (heterogeneous) | `list`           |

### Python → Uiua

| Python Type            | Uiua Type              |
| ---------------------- | ---------------------- |
| `int`                  | Scalar number          |
| `float`                | Scalar number          |
| `str`                  | Character array/string |
| `list` (homogeneous)   | Array                  |
| `list` (heterogeneous) | Box Array              |

## Development

### Requirements

- [rustup](https://rustup.rs/) (Rust installer)
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Set-up

```bash
# Clone
git clone https://github.com/KatieLG/python-uiua.git
cd python-uiua

# Install dependencies
uv sync

# Build and install
uv run maturin develop
```

### Dev Commands

| Command             | Purpose                                   |
| ------------------- | ----------------------------------------- |
| `make dev`          | Rebuild after making changes to Rust code |
| `make test`         | Run unit tests                            |
| `make lint`         | Run linters and type checkers             |
| `make format`       | Auto-format code                          |
| `make check`        | Format, lint, and test                    |
| `make build`        | Build wheel for distribution              |
| `make test-release` | Publish to TestPyPI                       |
| `make release`      | Publish to PyPI                           |

## Links

- [Uiua Language](https://www.uiua.org/)
- [PyO3 Documentation](https://pyo3.rs/)
- [Maturin Documentation](https://www.maturin.rs/)
