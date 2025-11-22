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
    """Test an empty stack returns an empty list."""
    result = uiua.uiua_stack("")
    assert isinstance(result, list)
    assert result == []


@pytest.mark.parametrize(
    "code,expected_stack",
    [("1 2 3 4 5", [5, 4, 3, 2, 1]), ("1_1 2_2", [[2, 2], [1, 1]])],
)
def test_uiua_stack_vs_eval(code: str, expected_stack: list) -> None:
    """Test the final element of the bottom to top stack is what eval returns."""
    stack_result = uiua.uiua_stack(code)
    eval_result = uiua.uiua_eval(code)

    assert stack_result == expected_stack
    assert eval_result == expected_stack.pop()
