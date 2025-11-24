import pytest

from pyuiua import Uiua


@pytest.mark.parametrize(
    "code,expected",
    [
        ("{1}", [1]),
        ("{42}", [42]),
        ('{"Hello"}', ["Hello"]),
        ("{3.14}", [3.14]),
        ("¤[1 2 3]", [[1, 2, 3]]),
    ],
)
def test_single_boxed_value_conversions(uiua: Uiua, code: str, expected: list) -> None:
    uiua.run(code)
    result = uiua.pop()
    assert isinstance(result, list)
    assert result == expected


@pytest.mark.parametrize(
    "code,expected",
    [
        ('{1 "Hello" 3.14 [2 3 4]}', [1, "Hello", 3.14, [2, 3, 4]]),
        ("{[1 2] [[3 4][5 6]] 7}", [[1, 2], [[3, 4], [5, 6]], 7]),
        ('{[1 2 3] [1.1 2.2 3.3] ["a" "b" "c"]}', [[1, 2, 3], [1.1, 2.2, 3.3], ["a", "b", "c"]]),
    ],
)
def test_boxed_array_mixed_types(uiua: Uiua, code: str, expected: list) -> None:
    uiua.run(code)
    assert uiua.pop() == expected
