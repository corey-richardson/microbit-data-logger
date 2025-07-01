#  These lines import the functions used to control
# the micro:bit.
from microbit import *
import log

# Create the columns you want to record using
# the `log.set_labels()` method:
pass


# The logger() function should record the x, y and z values
# of the accelerometer.
def logger():
    pass


# Initialise a boolean variable named 'logging' here which
# will be used as a conditional to determine if the logger() function
# should be called in the control loop
logging = None

# Inside the control loop, make it so the "A" button starts the
# recording and the "B" button stops the log from recording.
# Display relevant icons on the micro:bit's LED panel to indicate
# the mode.
while True:
    sleep(50)
