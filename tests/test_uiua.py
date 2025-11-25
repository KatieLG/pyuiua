import pytest

from pyuiua import Uiua, UiuaValue


def test_scalar_operations(uiua: Uiua) -> None:
    uiua.push([])
    uiua.push(5)
    uiua.push(3)
    uiua.run("+")
    uiua.run("×2")

    assert uiua.stack() == [[], 16]


@pytest.mark.parametrize(
    "python_value,uiua_code,expected_value",
    [
        ([1, 2, 3], "×2", [2, 4, 6]),
        ([1.5, 2.5], "/+", 4.0),
        (9, "+1", 10),
    ],
)
def test_array_operations(
    uiua: Uiua, python_value: UiuaValue, uiua_code: str, expected_value: UiuaValue
) -> None:
    uiua.push(python_value)
    uiua.run(uiua_code)
    assert uiua.pop() == expected_value
