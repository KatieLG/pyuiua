"""Python bindings for the Uiua programming language.

Supports executing Uiua code from python and manipulating the stack in either language.
Values are automatically converted between Python and Uiua types.

Example:
    >>> from pyuiua import Uiua
    >>> uiua = Uiua()
    >>> uiua.run("+ 1 2")
    >>> uiua.pop()
    3
"""

from typing import TypeAlias

UiuaValue: TypeAlias = int | float | str | list["UiuaValue"]
"""Type representing the values that pyuiua supports for python <-> uiua conversion.

Can be:

- int: (converts to Uiua Num/f64)

- float: (converts to Uiua Num/f64)

- str: (converts to a Uiua Char array)

- list: lists for flat or multi-dimensional arrays

Mixed int/float lists are converted to a float array in Uiua.
"""

class UiuaError(RuntimeError):
    """Exception raised when Uiua operations fail, such as:

    - Syntax errors in Uiua code passed to `run()`
    - Runtime errors during Uiua code execution
    - Calling `pop()` on an empty stack

    Example:
        >>> u = Uiua()
        >>> u.run("+ 1")  # Missing second argument
        UiuaError: ...
        >>> u.pop()  # Empty stack
        UiuaError: ...
    """

class Uiua:
    """A Uiua instance with a persistent stack.

    The Uiua class provides a Python interface to the Uiua language.
    It maintains a stack that persists between operations, allowing:
    - Pushing Python values onto the stack
    - Executing Uiua code that manipulates the stack
    - Pop results back to Python

    Example:
        >>> u = Uiua()
        >>> u.push([1, 2, 3, 4, 5])
        >>> u.run("/+") # Sum the array
        >>> u.pop()
        15
    """

    def __init__(self) -> None:
        """Create a new Uiua interpreter with an empty stack.

        Example:
            >>> u = Uiua()
            >>> len(u)
            0
        """
        ...

    def push(self, value: UiuaValue) -> None:
        """Push a Python value onto the Uiua stack.

        Args:
            value: A Python value to push.

        Raises:
            TypeError: If the value cannot be converted to a Uiua type.

        Example:
            >>> u = Uiua()
            >>> u.push(42)
            >>> u.push([1, 2, 3])
            >>> len(u)
            >>> u.stack()
            2
            [42, [1, 2, 3]]
        """
        ...

    def pop(self) -> UiuaValue:
        """Pop the top value from the stack and convert to a Python object.

        Returns:
            The top value from the stack as a Python value.

        Raises:
            UiuaError: If the stack is empty.

        Example:
            >>> u = Uiua()
            >>> u.push(42)
            >>> u.pop()
            42
            >>> u.pop()  # Stack is empty
            UiuaError: Failed to pop from stack: No values on stack
        """
        ...

    def stack(self) -> list[UiuaValue]:
        """Return all values on the stack as a Python list.

        Returns with the bottom of the stack at index 0 and the top at the end. The stack is not modified.

        Returns:
            A list containing all stack values, bottom to top.

        Example:
            >>> u = Uiua()
            >>> u.push(1)
            >>> u.push(2)
            >>> u.push(3)
            >>> u.stack()
            [1, 2, 3]
        """
        ...

    def run(self, code: str) -> None:
        """Execute Uiua code

        Runs the provided Uiua code, which has access to use and modify the current stack.

        Args:
            code: A string containing Uiua code to execute.

        Raises:
            UiuaError: If the code contains syntax errors or runtime errors.

        Example:
            >>> u = Uiua()
            >>> u.push(5)
            >>> u.push(3)
            >>> u.run("+")  # Add top two values
            >>> u.pop()
            8
        """
        ...

    def clear(self) -> None:
        """Remove all values from the stack.

        Example:
            >>> u = Uiua()
            >>> u.push(1)
            >>> u.push(2)
            >>> u.clear()
            >>> len(u)
            0
        """
        ...

    def __len__(self) -> int:
        """Get the number of values on the stack.

        Returns:
            The number of values currently on the stack.

        Example:
            >>> u = Uiua()
            >>> len(u)
            0
            >>> u.push(1)
            >>> len(u)
            1
        """
        ...

    def __repr__(self) -> str:
        """Generates a string representation of the Uiua instance.

        Returns:
            A string showing the current stack state

        Example:
            >>> u = Uiua()
            >>> repr(u)
            'Uiua(stack=[])'
            >>> u.push(42)
            >>> repr(u)
            'Uiua(stack=[42])'
        """
        ...

__all__ = ["Uiua", "UiuaError", "UiuaValue"]
