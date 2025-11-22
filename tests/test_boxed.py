import pytest


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
def test_single_boxed_value_conversions(uiua, code: str, expected: list) -> None:
    uiua.run(code)
    result = uiua.pop()
    assert isinstance(result, list)
    assert result == expected


def test_boxed_array_mixed_types(uiua) -> None:
    uiua.run('{1 "Hello" 3.14 [2 3 4]}')
    result = uiua.pop()
    assert isinstance(result, list)
    assert len(result) == 4
    assert result == [1, "Hello", 3.14, [2, 3, 4]]
    assert isinstance(result[0], int)
    assert isinstance(result[1], str)
    assert isinstance(result[2], float)
    assert all(isinstance(x, int) for x in result[3])


def test_mixed_nested_arrays(uiua) -> None:
    uiua.run("{[1 2] [[3 4][5 6]] 7}")
    result = uiua.pop()
    assert isinstance(result, list)
    assert len(result) == 3
    assert result == [[1, 2], [[3, 4], [5, 6]], 7]


def test_mixed_array_element_types(uiua) -> None:
    uiua.run('{[1 2 3] [1.1 2.2 3.3] ["a" "b" "c"]}')
    result = uiua.pop()
    assert isinstance(result, list)
    assert len(result) == 3
    assert result == [[1, 2, 3], [1.1, 2.2, 3.3], ["a", "b", "c"]]
    assert all(isinstance(x, int) for x in result[0])
    assert all(isinstance(x, float) for x in result[1])
    assert all(isinstance(x, str) for x in result[2])
