from microbit import *
import log, os

# Set up columns for logging
log.set_labels('x', 'y', 'z', 'strength')

def clear_log():
    logging = False
    display.show(Image.SWORD) 
    try:	
        os.remove("MY_DATA.HTM") # Check this actually works lol
    except FileNotFoundError:
        try:
            os.remove("MY_DATA.HTML")
        except FileNotFoundError:
            for i in range(4):
                display.show(Image.SAD)
                sleep(500)
                display.clear()
                sleep(250)
        
    display.show(Image.NO)

# Record the x, y, z and Pythagorean combined value 
def logger():
    log.add({
        'x': accelerometer.get_x(),
        'y': accelerometer.get_y(),
        'z': accelerometer.get_z(),
        'strength': accelerometer.get_strength()
    })

# Pre initialise 'logging' as False / OFF
logging = False

while True:
    sleep(50) # milliseconds
    # On "A" button pressed...
    # Clear the log, set logging to True and update displayed icon
    if button_a.is_pressed():
        clear_log()
        logging = True
        display.show(Image.YES)
        
    # On "B" button pressed...
    # Set logging to False and update displayed icon
    if button_b.is_pressed():
        logging = False
        display.show(Image.NO)

    # On "A" and "B" button pressed...
    # Clear the log
    if button_a.is_pressed() and button_b.is_pressed():
        clear_log()

    # If logging is set to True...
    # Call the logging function and record values
    if logging:
        logger()