# Rx

```py
# Imports go at the top
from microbit import *
import radio
radio.on()

def find_radio_group():
    display.show(Image.SAD)
    for radioGroup in range(0, 255):
        # display.show(radioGroup)
        radio.config(group=radioGroup)
        message = radio.receive()
        if message:
            display.show(Image.HAPPY)
            break


# EXTENSION
def decode(encrypted, shift):
    plain_text = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    for character in encrypted:
        if character in alphabet:
            value = alphabet.find(character)
            plain_text += alphabet[value - shift]
        elif character in digits:
            value = digits.find(character)
            plain_text += digits[value - shift]
        else:
            plain_text += character
    return plain_text
    

while True:
    find_radio_group()

    message = radio.receive()
    if not message:
        continue
    
    print(message)
    display.scroll(message)

    # EXTENSION
    for shift in range(0, 26):
        decrypted = decode(message, shift)
        print(decrypted)
```

---

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
            coded += str(alphabet[(value+shift) % 26])
        elif character in digits:
            value = digits.find(character)
            coded += str(digits[(value+shift) % 10])
        else:
            coded += character
    return coded
    
# You can use any group number between 0 and 255.
SECRET = 234
radio.config(group=SECRET)
radio.on()

SHIFT = 5
MESSAGE = ""
encoded_message = encode(MESSAGE, SHIFT) 

while True:
    radio.send(encoded_message)
    display.show(Image.HAPPY)
```

---

## MakeCode

![](/radio_message_decoder/MakeCode.PNG)

