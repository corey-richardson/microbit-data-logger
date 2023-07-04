# Rx

```py
from microbit import *
# Enable and set up radio configuration
import radio
radio.on()
radio.config(group=234)

# Iterate through letter in message and display
def display_message(message):
    for letter in message:
        display.show(letter)
        sleep(600)
        display.clear()
        sleep(50)

# EXTENSION
# Ceasar shift decoder
def decode(encrypted, shift):
    decoded = ""
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    NUMBERS = "0123456789"
    for character in encrypted:
        if character in ALPHABET:
            position = ALPHABET.find(character)
            decoded = decoded + ALPHABET[position - shift]
        elif character in NUMBERS:
            position = NUMBERS.find(character)
            decoded = decoded + NUMBERS[position - shift]
        else: # no shift needed
            decoded = decoded + character
    return decoded

# Initialse shift
shift = 0
# Control Loop
while True:
    # EXTENSION
    if button_a.was_pressed():
        shift += 1
        if shift > 9:
            shift = 0
    
    if button_b.was_pressed():
        message = radio.receive()
        if not message:
            continue

        display_message(message)
        display_message(decode(message, shift)) # EXTENSION
```

<div style="page-break-after: always;"></div>

## Tx

```py
# Imports go at the top
from microbit import *
import radio

def encode(plainText, shift):
    coded = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    for character in plainText:
        if character in alphabet:
            value = alphabet.find(character)
            coded = plain_text + str(alphabet[(value+shift) % 26])
        elif character in digits:
            value = digits.find(character)
            coded = plain_text + str(digits[(value+shift) % 10])
        else:
            coded = plain_text + character
    return coded
    
# You can use any group number between 0 and 255.
SECRET = ... # SET ME
radio.config(group=SECRET)
radio.on()

SHIFT = ... # SET ME
MESSAGE = ""
encoded_message = encode(MESSAGE, SHIFT) 

while True:
    radio.send(encoded_message)
    display.show(Image.HAPPY)
```
