"""Tests for boxed/heterogeneous array conversions to Python lists."""

from typing import Any

import pytest
import pyuiua as uiua


def test_mixed_scalar_types() -> None:
    """Test boxed array mixed scalar types."""
    result = uiua.uiua_eval('{1 "Hello" 3.14}')
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == 1
    assert isinstance(result[0], int)
    assert result[1] == "Hello"
    assert isinstance(result[1], str)
    assert result[2] == 3.14
    assert isinstance(result[2], float)


def test_mixed_nested_arrays() -> None:
    """Test conversion of boxed array with multidimensional elements."""
    result = uiua.uiua_eval('{[1 2] [[3 4][5 6]] 7}')
    assert isinstance(result, list)
    assert len(result) == 3
    assert result == [[1, 2], [[3, 4], [5, 6]], 7]


def test_mixed_array_element_types() -> None:
    """Test conversion of heterogeneous array with arrays of different element types."""
    result = uiua.uiua_eval('{[1 2 3] [1.1 2.2 3.3] ["a" "b" "c"]}')
    assert isinstance(result, list)
    assert len(result) == 3
    assert result == [[1, 2, 3], [1.1, 2.2, 3.3], ["a", "b", "c"]]
    assert all(isinstance(x, int) for x in result[0])
    assert all(isinstance(x, float) for x in result[1])
    assert all(isinstance(x, str) for x in result[2])
