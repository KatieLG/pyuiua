"""Tests for scalar value conversions."""

from typing import TypeAlias

import pytest
import pyuiua as uiua

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
    ],
)
def test_scalar_conversions(
    code: str, expected_type: type, expected_value: Scalar
) -> None:
    """Test basic scalar type conversions."""
    result = uiua.uiua_eval(code)
    assert isinstance(result, expected_type)
    assert result == expected_value
