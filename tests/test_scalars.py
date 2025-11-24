from typing import TypeAlias

import pytest

from pyuiua import Uiua, UiuaValue

Scalar: TypeAlias = int | float | str


@pytest.mark.parametrize(
    "value,expected_type",
    [
        (42, int),
        (0, int),
        (1000000, int),
        (-5, int),
        (3.14, float),
        ("Hello, World!", str),
        ("", str),
        ("Line1\nLine2", str),
    ],
)
def test_scalar_conversions(uiua: Uiua, value: UiuaValue, expected_type: type) -> None:
    uiua.push(value)
    result = uiua.pop()
    assert isinstance(result, expected_type)
    assert result == value
