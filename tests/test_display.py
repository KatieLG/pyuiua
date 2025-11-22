import pytest


@pytest.mark.parametrize(
    "code,expected_pretty,expected_repr",
    [
        ("1 2 3", "1 2 3", "Uiua(stack=[3, 2, 1])"),
        (
            "°△3_3",
            "╭─       \n╷ 0 1 2  \n  3 4 5  \n  6 7 8  \n        ╯",
            "Uiua(stack=[[[0, 1, 2], [3, 4, 5], [6, 7, 8]]])",
        ),
        ("¤1 2", "[1] 2", "Uiua(stack=[2, [1]])"),
        ("[□[1 2]]", "[1 2│]", "Uiua(stack=[[[1, 2]]])"),
    ],
)
def test_display(uiua, code: str, expected_pretty: str, expected_repr: str) -> None:
    uiua.run(code)
    assert uiua.pretty() == expected_pretty
    assert repr(uiua) == expected_repr
