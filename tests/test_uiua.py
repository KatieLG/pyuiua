import pytest

def test_push_pop_scalars(uiua):
    uiua.push(42)
    assert len(uiua) == 1

    result = uiua.pop()
    assert result == 42
    assert len(uiua) == 0


def test_push_pop_multiple_types(uiua):
    uiua.push(1)
    uiua.push(2.5)
    uiua.push("hello")
    uiua.push([1, 2, 3])

    assert len(uiua) == 4

    assert uiua.pop() == [1, 2, 3]
    assert uiua.pop() == "hello"
    assert uiua.pop() == 2.5
    assert uiua.pop() == 1


def test_stack_order(uiua):
    uiua.push(1)
    uiua.push(2)
    uiua.push(3)

    assert uiua.stack() == [3, 2, 1]


def test_operations(uiua):
    uiua.push(10)
    uiua.push(20)
    uiua.run("+")

    assert uiua.stack() == [30]


def test_run_multiple_operations(uiua):
    uiua.push([])
    uiua.push(5)
    uiua.push(3)
    uiua.run("+")
    uiua.run("×2")

    assert uiua.stack() == [16, []]


def test_clear_stack(uiua):
    uiua.push(1)
    uiua.push(2)
    uiua.push(3)

    uiua.clear()
    assert len(uiua) == 0


@pytest.mark.parametrize(
    "python_value,uiua_code,expected_value",
    [
        ([1, 2, 3], "×2", [2, 4, 6]),
        ([1.5, 2.5], "/+", 4.0),
        (9, "+1", 10),
    ],
)
def test_python_to_uiua_conversion(uiua, python_value: object, uiua_code: str, expected_value: object) -> None:
    uiua.push(python_value)
    uiua.run(uiua_code)
    assert uiua.pop() == expected_value


def test_mixed_types_boxed(uiua):
    uiua.push([1, "hello", 3.14])

    result = uiua.pop()
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == 1
    assert result[1] == "hello"
    assert result[2] == 3.14


def test_pop_empty_stack_error(uiua):
    with pytest.raises(RuntimeError, match="No values on stack"):
        uiua.pop()


def test_invalid_uiua_code(uiua):
    uiua.push(1)

    with pytest.raises(RuntimeError, match="Uiua error"):
        uiua.run("some invalid code")


def test_chained_operations(uiua):
    uiua.push([1, 2, 3, 4, 5])
    uiua.run(".")
    uiua.run("/+")

    assert uiua.pop() == 15
    assert uiua.pop() == [1, 2, 3, 4, 5]
