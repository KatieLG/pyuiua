import pytest
import pyuiua


@pytest.fixture
def uiua():
    return pyuiua.Uiua()
