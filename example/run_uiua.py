import pyuiua as uiua

# 10 factorial
ten_fact = uiua.uiua_eval("/×↘1⇡11")
print(f"10 factorial: {ten_fact}")

# 10 factorial fixed
ten_fact_array = uiua.uiua_eval("¤/×↘1⇡11")
print(f"10 factorial fixed: {ten_fact_array}")

# Boxed array of mixed types
boxed_array = uiua.uiua_eval('{1 "Hello" 3.14 [2 3 4]}')
print(f"boxed array: {boxed_array}")
