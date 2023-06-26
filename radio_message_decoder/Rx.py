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
