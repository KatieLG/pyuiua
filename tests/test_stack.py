import pytest

from pyuiua import Uiua, UiuaValue


@pytest.mark.parametrize(
    "code,expected",
    [
        ("1 2 3", [3, 2, 1]),
        ("1", [1]),
        ("+2 3", [5]),
        ('1 "hello" 3.14', [3.14, "hello", 1]),
        ("[1 2 3] [4 5 6]", [[4, 5, 6], [1, 2, 3]]),
    ],
)
def test_uiua_stack(uiua: Uiua, code: str, expected: list) -> None:
    """Test the stack returns as a list with the correct items"""
    uiua.run(code)
    result = uiua.stack()
    assert isinstance(result, list)
    assert result == expected


def test_push_stack_order(uiua: Uiua) -> None:
    uiua.push(0)
    uiua.push(1)
    uiua.push(2)

    assert uiua.stack() == [0, 1, 2]


@pytest.mark.parametrize(
    "code,expected_stack",
    [("1 2 3 4 5", [5, 4, 3, 2, 1]), ("1_1 2_2", [[2, 2], [1, 1]])],
)
def test_stack_pop(uiua: Uiua, code: str, expected_stack: list) -> None:
    """Test popping from the uiua stack gives the top item on the stack"""
    uiua.run(code)
    assert uiua.stack() == expected_stack
    assert uiua.pop() == expected_stack.pop()


@pytest.mark.parametrize(
    "value,expected_stack",
    [(42, [42]), ([1, 2, 3], [[1, 2, 3]]), ("hello", ["hello"])],
)
def test_push(uiua: Uiua, value: UiuaValue, expected_stack: list) -> None:
    """Test pushing values onto the uiua stack"""
    uiua.push(value)
    assert uiua.stack() == expected_stack


def test_clear_stack(uiua: Uiua) -> None:
    uiua.push(1)
    uiua.push(2)
    uiua.push(3)

    uiua.clear()
    assert len(uiua) == 0
    assert uiua.stack() == []
