import pytest

import pyuiua
from pyuiua import UiuaError, UiuaValue


@pytest.mark.parametrize(
    "code,input_args,expected_result",
    [
        ("+ 1 2", (), 3),
        ("/+", ([1, 2, 3, 4, 5],), 15),
        ("+", (10, 20), 30),
        ("1 2 3", (), (1, 2, 3)),
        ("", (), None),
        ("×2", ([1, 2, 3],), [2, 4, 6]),
        ("∩+", (1, 2, 3, 4), (3, 7)),
        ('"hello"', (), "hello"),
        ("↯2_3⇡6", (), [[0, 1, 2], [3, 4, 5]]),
        ("/×⇡₁10", (), 3628800),
    ],
)
def test_eval(code: str, input_args: tuple[UiuaValue, ...], expected_result: UiuaValue) -> None:
    assert pyuiua.eval(code, *input_args) == expected_result


def test_eval_syntax_error() -> None:
    with pytest.raises(UiuaError):
        pyuiua.eval("+ 1")
