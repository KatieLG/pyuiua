from typing import TypeAlias

import pytest

from pyuiua import Uiua

Scalar: TypeAlias = int | float | str


@pytest.mark.parametrize(
    "code,expected_type,expected_value",
    [
        ("42", int, 42),
        ("0", int, 0),
        ("1000000", int, 1000000),
        ("¯5", int, -5),
        ("3.14", float, 3.14),
        ("1.5", float, 1.5),
        ('"Hello, World!"', str, "Hello, World!"),
        ('""', str, ""),
        ('"Hello"', str, "Hello"),
        ('"Hello World"', str, "Hello World"),
        ('"Line1\\nLine2"', str, "Line1\nLine2"),
    ],
)
def test_scalar_conversions(
    uiua: Uiua, code: str, expected_type: type, expected_value: Scalar
) -> None:
    uiua.run(code)
    result = uiua.pop()
    assert isinstance(result, expected_type)
    assert result == expected_value
