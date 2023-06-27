What will the output of the following code be?

```py
def do_something(argument):
    return argument[::-1]

def do_something_else(argument):
    argument = str(argument)
    a = argument[0:3]
    b = argument[-1]
    return a, b

value = ""
# start value, end_value (exclusive), step
for i in range(6, 1, -1):
    value += str(i)

value = int(do_something(value)) // 10

radio_group, shift = do_something_else(value)

print(f"Connect your micro:bit to group {radio_group}.")
print(f"The Caesar Cipher is using a shift value of {shift}.")
```
