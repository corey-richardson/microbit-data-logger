from microbit import *

display.show(Image.HAPPY)

while True:
    sleep(50) # milliseconds
    print(accelerometer.get_values())