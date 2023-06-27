# Receiver Notes and Hints

---

[python.microbit.org/v/3/](https://python.microbit.org/v/3/)

Start by importing all the modules / dependencies you will need to complete the task; you want to use the `radio` module.

Enable the radio on the micro:bit.
> Reference > Radio > On and Off

The radio channel needs to be set to the same as the micro:bit transmitting the message.
> Reference > Radio > Groups

Next comes the control loop. The control loop is the `while True` loop that will run infinitely whilst the device is powered.

When a button is pressed, attempt to `receive` a message. Assign this to button `B`.
> Reference > Buttons > Button was pressed <br>
> Reference > Radio > Receive a message

If you dont receive a message with content, `continue` to the next iteration of the `while` loop. <br>
The *logical operator* `not` can be used here to determine if the variable has no value: `if not {variable_name}:`
> The keyword `continue` can be used here to skip the remaining code in the loop and move on to the next iteration to try again. <br>

If you have received a message, output it to the console and / or to the LED panel.
> Reference > Display > Scroll

This section of the code should look like:
```
while true
    call find_radio_group
    receive message
    if message is empty
        continue to next iteration
    output message
```

A function is a "chunk" of code that you can use over and over again, rather than writing it out multiple times. Functions enable programmers to break down or *decompose* a problem into smaller chunks, each of which performs a particular task. The basic structure for a function in Python is as so:
```py
def function_name(arg1, arg2):
    ...
```
> Reference > Functions

On second thought, you find that the `scroll` method doesn't give you enough time to record the message being output by the micro:bit. Replace this line with a function call to `display_message`, passing in the `message` as an argument. <br>
Now, back towards the start of your program, define the function you have just called. <br>
In this function, *iterate* through each `letter` in `message` and use the `display.show()` method to output this letter to the LED panel.
> Reference > Display > Show

You can change the amount of time each letter is displayed for with a second parameter in your call to `display.show()` - read the *documentation* to find out what this parameter is called.
> Reference > Display > Show > More

---

## Extension

> This extension assumes some level of confidence in Python. It can also be completed on paper if preferred.

What does `"ifmmp xpsme!"` mean? <br>
The message is encrypted using a Ceasar Shift!

A Ceasar Shift Decoder can be written here as a function.

For a Ceasar Shift we have two arguments to pass in:
- The Encrypted Message
- The Magnitude of the Shift

> `"a"` --> `"b"` would have a shift magnitude of `1`.

In psuedo-code this function would look like:
```
define 'decode' with parameters 'encrypted' and 'shift'
    initialise empty string called 'decoded'
    initialise string 'ALPHABET'
    initialise string 'NUMBERS'
    for character in encrypted message
        if character is in the ALPHABET
            find position of the character in 'ALPHABET'
            add the letter at index 'value - shift' to 'decoded'
        else if character is in the 'number' string
            find position of the character in 'NUMBERS'
            add the letter at index 'value - shift' to 'decoded'
        else
            # assume value is punctuation, doesn't need to be shifted.
            add the character to 'decoded'
```
```py
decoded = ""
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"
```
> Constants are unchanging variables. They are written in all capital letters with underscores separating words. Examples include `MAX_OVERFLOW` and `TOTAL`. <br>
> You may need to see the notes on the `.find()` method towards the back of this document. Alternatively, you could find *documentation* explaining the usage of this method online!


You should then to call the `decode` function from the control loop as an argument of 'display_message'. Add this to the area where you receive the message when a button is pressed.
> Functions can be arguments to other *functions* and *procedures*. <br>
> ```py
> function_one( function_two(f2_arg_one, f2_arg_two) )
> ```

Add functionality to set the magnitude of the `shift`. This could be done with button presses which increment a *counter variable*. Assign this to button `A`. Don't allow this value to be greater than 9. 
```
initialise shift to 0
while true (control loop)
    ...
    on button press 
        add 1 to shift
        if shift bigger than 9
            reset shift to 0
```

---

### String `.find()` Method

The `.find()` method finds the first occurrence of the specified value. <br>
The `.find()` method returns `-1` if the value is not found.
```py
company = "Collins Aerospace"
print( company.find("A") ) ## prints "8"
```

### Indexing Into a List

Use square brackets after the list name to index into a list. Python uses zero-indexing for lists.
```py
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
print(ALPHABET[0]) # prints "a"
print(ALPHABET[1]) # prints "b"
print(ALPHABET[-1]) # prints "z"
```

---

## Portfolio

- [ ] Importing Modules
- [ ] `if` Statements
- [ ] `if-elif-else` Statements
- [ ] `while` Loops
- [ ] `for` Loops
- [ ] `continue` Keyword
- [ ] Functions and `return`ing from functions
- [ ] User Input