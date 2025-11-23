import pytest

from pyuiua import Uiua, UiuaError


def test_pop_empty_stack_error(uiua: Uiua) -> None:
    with pytest.raises(UiuaError):
        uiua.pop()


@pytest.mark.parametrize("code", ["invalid syntax", "+ 1"])
def test_invalid_uiua_code(uiua: Uiua, code: str) -> None:
    with pytest.raises(UiuaError):
        uiua.run(code)


@pytest.mark.parametrize("unsupported_type", [{"key": "value"}, object(), {1, 2, 3}])
def test_invalid_python_type(uiua: Uiua, unsupported_type: dict | object | set) -> None:
    with pytest.raises(TypeError):
        uiua.push(unsupported_type)
