import pytest

from pyuiua import Uiua, UiuaError, UiuaValue


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
def test_stack(uiua: Uiua, code: str, expected: list) -> None:
    """Test stack() returns values bottom-to-top."""
    uiua.run(code)
    assert uiua.stack() == expected


@pytest.mark.parametrize(
    "input_value,code,expected",
    [
        ([1, 2, 3], "⊃⊢⊣", [3, 1]),
        ([1, 2], "°⊟", [2, 1]),
        ([1, 2, 3, 4, 5], "/+", [15]),
        ("hello", "⇌", ["olleh"]),
    ],
)
def test_stack_operations(uiua: Uiua, input_value: UiuaValue, code: str, expected: list) -> None:
    """Test push → run → stack cycle."""
    uiua.push(input_value)
    uiua.run(code)
    assert uiua.stack() == expected


def test_len(uiua: Uiua) -> None:
    assert len(uiua) == 0
    uiua.push(1)
    assert len(uiua) == 1
    uiua.push(2)
    uiua.push(3)
    assert len(uiua) == 3


def test_clear(uiua: Uiua) -> None:
    uiua.push(1)
    uiua.push(2)
    uiua.clear()
    assert len(uiua) == 0
    assert uiua.stack() == []


def test_run_invalid_code(uiua: Uiua) -> None:
    with pytest.raises(UiuaError):
        uiua.run("invalid syntax")
