from microbit import *

# Happy whoop whoop
display.show(Image.HAPPY)

# Control loop
while True:
    # Every n milliseconds, print the x, y and z values given by the 
    # onboard accelerometer.
    # By printing these values, you output them to the serial port.
    sleep(50) # milliseconds
    print(accelerometer.get_values())