import pyuiua

uiua = pyuiua.Uiua()

# Run arbitrary Uiua code
uiua.run('&p "Hello from Uiua!"')

# Add values to the stack from python
uiua.push(1)
uiua.push([1, 2, 3])
uiua.push(["mixed types", 42, 3.14])

# Retrieve and print the current stack
print(f"{uiua.stack()=}")

# See the stack when printing the repr
print(f"{uiua=}")

# Pop from the stack
print(f"{uiua.pop()=}")

# Run a command against the python added values on the stack
print(f"Running + to sum top two values on the stack ({uiua.stack()})")
uiua.run("+")
print(f"{uiua.pop()=}")

# Clear the stack
uiua.clear()
print(f"Stack cleared: {uiua.stack()=}")
