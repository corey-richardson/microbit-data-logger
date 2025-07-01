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
            coded += str(alphabet[(value + shift) % 26])
        elif character in digits:
            value = digits.find(character)
            coded += str(digits[(value + shift) % 10])
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
