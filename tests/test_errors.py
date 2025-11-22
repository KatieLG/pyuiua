"""Tests for error handling."""

import pytest
import pyuiua as uiua


def test_invalid_code_raises_error() -> None:
    """Test that invalid code raises RuntimeError."""
    with pytest.raises(RuntimeError):
        uiua.uiua_eval("invalid syntax")
