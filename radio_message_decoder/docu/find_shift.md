## What will the output of the following code be?

```py
def do_something(argument_one):
    return argument_one[::-1]
```
What is the effect of this function? ______________________________________________________

```py
def do_something_else(argument_two):
    argument_two = str(argument_two)
    a = argument_two[0:3]
    b = argument_two[-1]
    return a, b
```
What is the effect of this function? ______________________________________________________

```py
value = ""
for i in range(6, 1, -1):
    value = ''.join([value, str(i)])
```
Value = __________

```py
value = int(do_something(value)) // 10
```
Value = __________

```py
radio_group, shift = do_something_else(value)
```
```py
print(f"Connect your micro:bit to group {radio_group}.")
print(f"The Caesar Cipher is using a shift magnitude of {shift}.")
```
Radio Group = ____________________ Shift = ____________________

---

Documentation Hunt: Feel free to use the internet or the notes at the back of your packs to understand the code! <br>
Here are some of the key things you may want to focus on... <br>
`[::-1]`, `[0:3]`, `[-1]`, `range(a, b, c)`, `''.join([a, b])`, `//`