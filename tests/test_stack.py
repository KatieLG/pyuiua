import pytest

from pyuiua import Uiua


@pytest.mark.parametrize(
    "code,expected",
    [
        ("1 2 3", [1, 2, 3]),
        ("1", [1]),
        ("+2 3", [5]),
        ('1 "hello" 3.14', [1, "hello", 3.14]),
        ("[1 2 3] [4 5 6]", [[1, 2, 3], [4, 5, 6]]),
    ],
)
def test_uiua_stack(uiua: Uiua, code: str, expected: list) -> None:
    """Test the stack returns as a list with the correct items"""
    uiua.run(code)
    result = uiua.stack()
    assert isinstance(result, list)
    assert result == expected


def test_uiua_stack_empty(uiua: Uiua) -> None:
    """Test that an empty stack gives an empty list"""
    uiua.run("")
    result = uiua.stack()
    assert isinstance(result, list)
    assert result == []


@pytest.mark.parametrize(
    "code,expected_stack",
    [("1 2 3 4 5", [1, 2, 3, 4, 5]), ("1_1 2_2", [[1, 1], [2, 2]])],
)
def test_uiua_stack_vs_pop(uiua: Uiua, code: str, expected_stack: list) -> None:
    """Test popping from the uiua stack gives the top item on the stack"""
    uiua.run(code)
    assert uiua.stack() == expected_stack
    assert uiua.pop() == expected_stack[0]
