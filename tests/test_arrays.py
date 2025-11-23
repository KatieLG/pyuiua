import pytest

from pyuiua import Uiua


@pytest.mark.parametrize(
    "code,expected_item_type,expected",
    [
        ("[1 2 3]", int, [1, 2, 3]),
        ("⇡5", int, [0, 1, 2, 3, 4]),
        ("[1.5 2.5 3.5]", float, [1.5, 2.5, 3.5]),
        ("[]", None, []),
    ],
)
def test_flat_array_conversions(
    uiua: Uiua, code: str, expected_item_type: type | None, expected: list
) -> None:
    uiua.run(code)
    result = uiua.pop()
    assert isinstance(result, list)
    assert result == expected
    assert all(isinstance(x, expected_item_type) for x in result)


@pytest.mark.parametrize(
    "code,expected",
    [
        # 2D arrays
        ("[[1 2] [3 4]]", [[1, 2], [3, 4]]),
        ("↯3_3 ⇡9", [[0, 1, 2], [3, 4, 5], [6, 7, 8]]),
        # 3D arrays
        ("[[[1 2][3 4]][[5 6][7 8]]]", [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]),
        # 2D float array
        ("↯2_2 [1.1 2.2 3.3 4.4]", [[1.1, 2.2], [3.3, 4.4]]),
    ],
)
def test_multidimensional_array_conversions(uiua: Uiua, code: str, expected: list) -> None:
    uiua.run(code)
    result = uiua.pop()
    assert isinstance(result, list)
    assert result == expected


@pytest.mark.parametrize(
    "stack_value",
    [
        "hello world",
        ["hello world"],
        ["h", "e", "ll", "o", "world"],
        [["h", "e"], "llo", ["world"]],
    ],
)
def test_character_array_conversions(uiua: Uiua, stack_value: str | list) -> None:
    """Test that converting string values between python & uiua gets dimension correct"""
    uiua.push(stack_value)
    result = uiua.pop()
    assert result == stack_value
