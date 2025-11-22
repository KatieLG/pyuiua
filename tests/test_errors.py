import pytest


def test_invalid_code_raises_error(uiua) -> None:
    with pytest.raises(RuntimeError) as e:
        uiua.run("invalid uiua syntax")

    assert "Uiua error" in str(e.value)
