import pytest

from pyuiua import Uiua


def test_invalid_code_raises_error(uiua: Uiua) -> None:
    with pytest.raises(RuntimeError) as e:
        uiua.run("invalid uiua syntax")

    assert "Uiua error" in str(e.value)
