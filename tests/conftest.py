import pytest

from pyuiua import Uiua


@pytest.fixture
def uiua() -> Uiua:
    return Uiua()
