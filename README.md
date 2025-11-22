# python-uiua

A Python binding for [Uiua](https://www.uiua.org/), a stack-based array programming language written in Rust. 
This package allows executing Uiua directly from Python.

## Requirements

- Python 3.9 or higher

## Installation

```bash
pip install pyuiua
```

## Example Usage

```python
import pyuiua as uiua

# Execute Uiua code and get the result
result = uiua.uiua_eval("/×↘1⇡11")  # Calculate 10 factorial
print(result)  # Output: 3628800

# Arrays are automatically converted to Python lists
array_result = uiua.uiua_eval("¤/×↘1⇡11")  # 10 factorial as array
print(array_result)  # Output: [3628800]

# Multi-dimensional arrays
matrix = uiua.uiua_eval("⇡3 3")  # Create a 3x3 range
print(matrix)  # Output: [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
```

## Development

### Requirements

- Python 3.9 or higher
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

## Type Conversions

| Uiua Type               | Python Type      |
|-------------------------|------------------|
| Scalar number           | `int` or `float` |
| Scalar char             | `str`            |
| Scalar byte             | `int`            |
| 1D Array                | `list`           |
| Multi-dimensional Array | Nested `list`    |

## Links

- [Uiua Language](https://www.uiua.org/)
- [PyO3 Documentation](https://pyo3.rs/)
- [Maturin Documentation](https://www.maturin.rs/)
