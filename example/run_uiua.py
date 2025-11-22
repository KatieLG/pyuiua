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

# Pop from the stack
print(f"{uiua.pop()=}")

# Run a command against the python added values on the stack
print(f"Running + to sum top two values on the stack ({uiua.stack()})")
uiua.run('+')
print(f"{uiua.pop()=}")

# Uses the uiua display representation
uiua.push("Hello")
uiua.run("°△3_3")
print(f"{uiua=}")
