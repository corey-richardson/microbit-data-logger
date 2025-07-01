from microbit import *
import log

# Set up columns for logging
log.set_labels('x', 'y', 'z')


# Record the x, y, z values
def logger():
    log.add({
        'x': accelerometer.get_x(),
        'y': accelerometer.get_y(),
        'z': accelerometer.get_z()
    })


# Pre initialise 'logging' as False / OFF
logging = False

while True:
    sleep(50)  # milliseconds
    # On "A" button pressed...
    # Clear the log, set logging to True and update displayed icon
    if button_a.is_pressed():
        logging = True
        display.show(Image.YES)

    # On "B" button pressed...
    # Set logging to False and update displayed icon
    if button_b.is_pressed():
        logging = False
        display.show(Image.NO)

    # If logging is set to True...
    # Call the logging function and record values
    if logging:
        logger()
