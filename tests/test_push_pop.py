import pytest

from pyuiua import Uiua, UiuaError, UiuaValue


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
def test_push_scalar(uiua: Uiua, value: UiuaValue, expected_type: type) -> None:
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
def test_push_bytes(uiua: Uiua, value: bytes, expected_result: list[int]) -> None:
    uiua.push(value)
    result = uiua.pop()
    assert isinstance(result, list)
    assert all(isinstance(b, int) for b in result)
    assert result == expected_result


@pytest.mark.parametrize(
    "value,expected_item_type",
    [
        ([1, 2, 3], int),
        ([10, 20, 30, 40, 50], int),
        ([1.5, 2.5, 3.5], float),
        ([2234], float),
    ],
)
def test_push_array(uiua: Uiua, value: list[UiuaValue], expected_item_type: type) -> None:
    uiua.push(value)
    result = uiua.pop()
    assert isinstance(result, list)
    assert result == value
    assert all(isinstance(x, expected_item_type) for x in result)


@pytest.mark.parametrize(
    "value",
    [
        "hello world",
        ["hello world"],
        ["h", "e", "ll", "o", "world"],
        [["h", "e"], "llo", ["world"]],
    ],
)
def test_push_string_arrays(uiua: Uiua, value: str | list[UiuaValue]) -> None:
    uiua.push(value)
    assert uiua.pop() == value


@pytest.mark.parametrize("unsupported", [{"key": "value"}, object(), {1, 2, 3}])
def test_push_unsupported_type(uiua: Uiua, unsupported: dict | object | set) -> None:
    with pytest.raises(TypeError):
        uiua.push(unsupported)  # type: ignore


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
def test_pop_scalar(uiua: Uiua, code: str, expected_type: type, expected_value: UiuaValue) -> None:
    uiua.run(code)
    result = uiua.pop()
    assert isinstance(result, expected_type)
    assert result == expected_value


@pytest.mark.parametrize(
    "code,expected_item_type,expected",
    [
        ("[1 2 3]", int, [1, 2, 3]),
        ("⇡5", int, [0, 1, 2, 3, 4]),
        ("[1.5 2.5 3.5]", float, [1.5, 2.5, 3.5]),
        ("[]", object, []),
        ("[[1 2] [3 4]]", list, [[1, 2], [3, 4]]),
        ("↯3_3 ⇡9", list, [[0, 1, 2], [3, 4, 5], [6, 7, 8]]),
        ("[[[1 2][3 4]][[5 6][7 8]]]", list, [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
        ("↯2_2 [1.1 2.2 3.3 4.4]", list, [[1.1, 2.2], [3.3, 4.4]]),
    ],
)
def test_pop_array(
    uiua: Uiua, code: str, expected_item_type: type, expected: list[UiuaValue]
) -> None:
    uiua.run(code)
    result = uiua.pop()
    assert isinstance(result, list)
    assert result == expected
    assert all(isinstance(x, expected_item_type) for x in result)


@pytest.mark.parametrize(
    "code,expected",
    [
        ("□[1 2]", [1, 2]),
        ("{42}", [42]),
        ('{"Hello"}', ["Hello"]),
        ("{3.14}", [3.14]),
        ("¤[1 2 3]", [[1, 2, 3]]),
        ('{1 "Hello" 3.14 [2 3 4]}', [1, "Hello", 3.14, [2, 3, 4]]),
        ("{[1 2] [[3 4][5 6]] 7}", [[1, 2], [[3, 4], [5, 6]], 7]),
        ('{[1 2 3] [1.1 2.2 3.3] ["a" "b" "c"]}', [[1, 2, 3], [1.1, 2.2, 3.3], ["a", "b", "c"]]),
        ("□{□[1 2] □1 3}", [[1, 2], 1, 3]),
    ],
)
def test_pop_boxed(uiua: Uiua, code: str, expected: list) -> None:
    uiua.run(code)
    result = uiua.pop()
    assert isinstance(result, list)
    assert result == expected


def test_pop_empty_stack(uiua: Uiua) -> None:
    with pytest.raises(UiuaError):
        uiua.pop()
