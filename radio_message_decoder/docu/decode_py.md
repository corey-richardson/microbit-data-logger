### Ceasar Shift Decoder - Python

```py
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

print(decode("ifmmp xpsme", 1))
```
```
hello world
```