"""Tests for stack operations."""

import pytest
import pyuiua as uiua


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
def test_uiua_stack(code: str, expected: list) -> None:
    """Test uiua_stack returns entire stack as list."""
    result = uiua.uiua_stack(code)
    assert isinstance(result, list)
    assert result == expected


def test_uiua_stack_empty() -> None:
    """Test uiua_stack with empty stack returns empty list."""
    result = uiua.uiua_stack("")
    assert isinstance(result, list)
    assert result == []


def test_uiua_stack_vs_eval() -> None:
    """Test that uiua_stack returns all values while uiua_eval returns top."""
    code = "1 2 3 4 5"
    stack_result = uiua.uiua_stack(code)
    eval_result = uiua.uiua_eval(code)

    assert stack_result == [5, 4, 3, 2, 1]
    assert eval_result == 1
