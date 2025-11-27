import pytest

from pyuiua import Uiua, UiuaValue


@pytest.mark.parametrize(
    "value,expected_type",
    [
        (42, int),
        (0, int),
        (1, int),
        (1000000, float),
        (-5, float),
        (3.14, float),
        ("Hello, World!", str),
        ("", str),
        ("Line1\nLine2", str),
        (1j + 3, complex),
    ],
)
def test_scalar_to_uiua(uiua: Uiua, value: UiuaValue, expected_type: type) -> None:
    uiua.push(value)
    result = uiua.pop()
    assert isinstance(result, expected_type)
    assert result == value


@pytest.mark.parametrize(
    "value,expected_result",
    [
        (b"abcd", [97, 98, 99, 100]),
        (b"", []),
        (b"\x00\xff", [0, 255]),
    ],
)
def test_bytes(uiua: Uiua, value: UiuaValue, expected_result: list[int]) -> None:
    uiua.push(value)
    result = uiua.pop()
    assert isinstance(result, list)
    assert all(isinstance(b, int) for b in result)
    assert result == expected_result


@pytest.mark.parametrize(
    "code,expected_type,expected_value",
    [
        ("3.14", float, 3.14),
        ("1", int, 1),
        ("256", float, 256),
        ('"Hello, World!"', str, "Hello, World!"),
        ("¯7", float, -7),
        ("2.71828", float, 2.71828),
        ("□2", int, 2),
        ("□255", int, 255),
        ("□1234", float, 1234),
        ("ℂ2 1", complex, 1 + 2j),
    ],
)
def test_scalar_to_python(
    uiua: Uiua, code: str, expected_type: type, expected_value: UiuaValue
) -> None:
    uiua.run(code)
    result = uiua.pop()
    assert isinstance(result, expected_type)
    assert result == expected_value
