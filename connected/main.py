from microbit import *

while True:
    sleep(50) # milliseconds
    print(accelerometer.get_values())