# Data Logger Project

---

## Contents

> UPDATE THIS

---

## Aims

- Flash software to the *BBC micro:bit* that will record accelerometer data.
- This could either be done via multiple micro:bits using radio transmissions as shown [here](https://microbit.org/projects/make-it-code-it/python-wireless-data-logger/) or via the `log` module as described [here](https://microbit.org/get-started/user-guide/data-logging/); this would only require one device.
- Then, write a Python script to do analysis on and plot the recorded data.

An interesting scenario to record could be archery. This would show how movement / stabilisation changes throughout the shot process and the vibrations and forces involved during the loose of an arrow. This would be similar to a commercial product called the "Mantis X8 Archery Training Tool for Marksmanship" which measures shot feedback, allowing the archer to visualise movements that the human eye will not see.

Could also be worth creating another script that works connected to a computer and plots the data in real-time.  This may be able to be done with "Mu" Code Editor.

---

## Concerns

- [x] Is micro:bit storage non-volatile? *(Will the logs be erased when it is unplugged from power?)*
> Data is stored on your micro:bit even when the power is disconnected. It's easy to access - no software is needed. Plug your micro:bit in to a computer, look in the MICROBIT drive and double-click the MY_DATA file to open it in a web browser.

- [ ] Does the micro:bit have enough storage space to record data for the time frames I'm hoping to record?
> Memory: 128 KB. Flash space: 512 KB.

- [ ] Need to verify if micro:bit will work on work laptop.
    - If no, need to get USB encryption exception permissions.

![teams_EA](/README_assets/teams_EA.PNG)

- [ ] Can Mu be installed on a work laptop?
    - More specifically, is Mu *<u>allowed</u>* to be installed on a work laptop?

- [ ] Can I install Pip / PyPI Modules on a work laptop?
    - I believe I have all dependencies other than `PySerial` installed, would a USB transfer from an external device be possible?

---

## Relevant Practice Projects

- [Meet your micro:bit](https://microbit.org/projects/make-it-code-it/meet-your-microbit/?editor=python)
- [Python Data Logger](https://microbit.org/projects/make-it-code-it/python-wireless-data-logger/) - Modify to use `log` module, only one device.
    - Connect the receiver micro:bit to a computer by USB and flash the logger program on to it using the Mu Python editor app.
    - Mu saves the numerical data as a CSV (comma separated values) file in your computer's home folder. Look in 'mu_code' and then the 'data_capture' folder.
    - You can open the CSV file in a spreadsheet program to analyse. If you delete the second and third time columns, leaving only the first, you can plot the data on a scatter graph in your spreadsheet showing how the forces change over time.
    - [codewith.mu](https://codewith.mu/)
- [Max-min temperature logger
](https://microbit.org/projects/make-it-code-it/maxmin-temperature-logger/)
    - How to use Python to read and write data to non-volatile storage that stays on your micro:bit even when the power is removed

---

## Research

### Initial Scripting

```py
from microbit import *
import log, os

# Set up columns for logging
log.set_labels('x', 'y', 'z', 'strength')

def clear_log():
    logging = False
    display.show(Image.SWORD) 	
    os.remove("MY_DATA.HTM") # Check this actually works lol
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
```

Would a single button work better to activate and deactivate logging?
```py
logging = False
while True:
    if button_a.is_pressed():
        logging = not logging
```

### Scheduled Log Entries

Is there any way I could use *Scheduled Log Entries" here?
```py
import log

@run_every(s=30)
def log_data():
    log.add({
      'temperature': temperature(),
      'sound': microphone.sound_level(),
      'light': display.read_light_level()
    })
    
while True:
    sleep(100000)
```

### Clearing the Log

> In *MakeCode*, the 'delete log' block contains two options: the fast delete and the full delete, as shown in the image below.
> - A "fast" delete method will invalidate your data and mark the MY_DATA log file as empty, but the data log remains in the file. It is the quickest method to erase the data log from your micro:bit, but it is not the cleanest as the data still remains in the file.
> - A 'full' delete method will clean all the data from the MY_DATA log file. It is the cleanest method to erase data logs. This process will take some time, but it is more efficient as it cleans the micro:bit completely.

How do I delete log with Python? `os.remove()`?
```py
def clear_log():
    logging = False
    display.show(Image.SWORD) 	
    os.remove("MY_DATA.HTM") # Check this actually works lol
    display.show(Image.NO)
```

### Realtime Plotting with Mu Code Editor

Mu Code Editor could be used to provide a real time plot of x, y and z values. [Plotter Guide](https://codewith.mu/en/tutorials/1.2/plotter)

[Mu and micro:bit](https://codewith.mu/en/tutorials/1.2/microbit)

![Mu Plotter Anim](https://codewith.mu/img/en/tutorials/python3_plotter.gif)

![Flashing](https://codewith.mu/img/en/tutorials/microbit_flash.gif)

![Moving Files between Devices](https://codewith.mu/img/en/tutorials/microbit_files.gif)

```py
from microbit import *

while True:
    sleep(50) # milliseconds
    print(accelerometer.get_values())
    # Use CodeWithMu to plot real time


# Ensure .get_values() outputs in correct format:
# (x, y, z)
# NOT
# x, y, z
# [x, y, z]
```

### Realtime Plotting with Matplotlib

**Serial Data**

You can send and receive data over serial on the micro:bit.
In Python, the `print` statement sends a string from the micro:bit to the connected computer over serial.

```
pip install pyserial
```

- Baud rate  = 115200
- Data = 8 bits
- Parity  = none
- Stop  = 1 bit
<br><br>
- Initialise Serial Port
- Create Figure for Plotting
- Initialise 'animate' function to be called by `FuncAnimation`
    - Parse Serial Data
    - Add x, y and z to lists
    - Limit lists to 'n' values
    - Draw lists
    - Format Plot (Titles, Labels, etc)
- Set up plot to call animate() 

---

## Visualing the micro:bit Data - Connected

### Connected main.py

This script is flashed onto the BBC micro:bit

```py
from microbit import *

while True:
    sleep(50) # milliseconds
    print(accelerometer.get_values())
```

The `print` command outputs to the USB serial port to be picked up by the connected laptop or computer.

### Connected Realtime Visualiser

**Imports:** 

```py
from matplotlib import pyplot as plt
from matplotlib import animation
import serial
```

**Configuration:**

These constants define the serial port to attempt a connection to, the [Baud Rate](https://en.wikipedia.org/wiki/Baud) of the board, the timeout bit, the number of datapoints to display at a time and the rate at which the plot will update.

$$\text{LIMIT} \times \text{RATE} = \text{Number of Seconds Displayed}$$

```py
# Windows Device Manager > Ports (COM & LPT) > "mbed Serial Port"
PORT = 'COM3'
BAUD_RATE = 115_200 # ENSURE THIS MATCHES VALUE IN DEVICE MANAGER
STOP = 1

LIMIT = 75
RATE = 5 # ms
```

**Connect to Serial Port:**

Create a connection to the board. If the connection fails to open, exit the program.
```py
ser = serial.Serial(PORT, BAUD_RATE, timeout=STOP)
ser.close()
ser.open()
```

**Create Figure to Plot:**

Create a figure and add a subplot at position `111`.
```py
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
```

**Initialise Lists for x, y and z Data:**

```py
xs, ys, zs = [0]*LIMIT, [0]*LIMIT, [0]*LIMIT
```

**Animate Function:**

Create the function `animate` that will get called as an argument in `FuncAnimate` later.

Read the line from the serial port connection. This is returned as a `byte` object so needs to be decoded with `.decode("utf-8")`. The parenthesis also need to be removed with `.strip()`. Then, cast the values to ints.

Create a list with length `LIMIT`. Append the current values to `xs`, `ys` and `zs`. Then, slice the list to only include the `n` most recent values, where `n` is `LIMIT`.

Once the lists have enough values in them, begin plotting.

```py
def animate(i, xs, ys, zs):
        
    line = ser.readline().decode("utf-8").strip("(").strip(")\r\n")
    x, y, z = line.split(",")
    x, y, z = int(x), int(y), int(z)
    
    print(x, y, z)
    
    idx = range(LIMIT)
    xs.append(x)
    ys.append(y)
    zs.append(z)
    
    xs = xs[-LIMIT:]
    ys = ys[-LIMIT:]
    zs = zs[-LIMIT:]
    
    if len(xs) == LIMIT:
        ax.clear()
        ax.plot(idx, xs, label="X")
        ax.plot(idx, ys, label="Y")
        ax.plot(idx, zs, label="Z")
        
    ax.set_ylim(-1500, 1500)
    plt.title("micro:bit Data Logger")
    plt.ylabel("Magnitude")
```

**Create and Plot Animation:**

Create the animation. This will call the `FuncAnimation` `animate` with arguments `xs`, `ys` and `zs` every `RATE` milliseconds. This occurs until the user causes a `KeyboardInterrupt` exception with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

```py
ani = animation.FuncAnimation(
    fig, 
    animate, fargs=(xs, ys, zs), 
    interval=RATE )

plt.show()

try:
    pass
except KeyboardInterrupt:
    ser.close()
```

### Connected Realtime Visualiser 3D

A lot of this code is repeated from the 2D visualiser. Some exceptions include:
- `RATE` and `LIMIT` values
    - I had to increase the `RATE` constant (which decreases the rate - 1/n) and decrease the `LIMIT` constant which controls how many datapoints are displayed in order to avoid overloading the animation function. Even now, eventually the animation falls out of sync with the micro:bit's movements.
- `ax = plt.axes(projection='3d')`
    - Creates a 3D Axis to plot data on.
- `ax.plot3D(xs, ys, zs)`
    - Creates a line plot with `xs`, `ys` and `zs` as data inputs.


```py
from matplotlib import pyplot as plt
from matplotlib import animation
import serial

# Windows Device Manager > Ports (COM & LPT) > "mbed Serial Port"
PORT = 'COM3'
BAUD_RATE = 115_200 # ENSURE THIS MATCHES VALUE IN DEVICE MANAGER
STOP = 1

LIMIT = 50
RATE = 50 # ms

ser = serial.Serial(PORT, BAUD_RATE, timeout=STOP)
ser.close()
ser.open()

fig = plt.figure()
ax = plt.axes(projection='3d')

xs, ys, zs = [0]*LIMIT, [0]*LIMIT, [0]*LIMIT


def animate(i, xs, ys, zs):
    
    line = ser.readline().decode("utf-8").strip("(").strip(")\r\n")
    x, y, z = line.split(",")
    x, y, z = int(x), int(y), int(z)
    
    print(x, y, z)
    
    idx = range(LIMIT)
    xs.append(x)
    ys.append(y)
    zs.append(z)
    
    xs = xs[-LIMIT:]
    ys = ys[-LIMIT:]
    zs = zs[-LIMIT:]
    
    if len(xs) == LIMIT:
        ax.clear()
        ax.plot3D(xs, ys, zs)
        
    ax.set_xlim(-1500, 1500)
    ax.set_ylim(-1500, 1500)
    ax.set_zlim(-1500, 1500)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
        
ani = animation.FuncAnimation(
    fig, 
    animate, fargs=(xs, ys, zs), 
    interval=RATE )

plt.show()

try:
    pass
except KeyboardInterrupt:
    ser.close()
```


---

## Visualing the micro:bit Data - Not Connected

### Process

1. Run the data logger via battery power.
2. When you use the data logging feature on the micro:bit V2, an HTML file is created on the `MICROBIT` drive called `MY_DATA` that lets you interact with the logged data.
3. View `MY_DATA` in your browser. The page displays a set of buttons to interact with the data and a table containing the data that has been logged so far.
4. Click the <kbd>Download</kbd> button. This downloads the data in `.csv` format using a period `.` as the delimiter.
5. Run the `/not_connected/visualiser.py` script and follow any instructions that appear on screen.

### Not Connected main.py

**Imports:**

```py
from microbit import *
import log, os
```

**Initialise the columns to log to:**

```py
# Set up columns for logging
log.set_labels('x', 'y', 'z', 'strength')
```

**Define the `logger` function:**

This is the function that records the `x`, `y`, `z` and `strength` values from the accelerometer into `"MY_DATA"`.
```py
# Record the x, y, z and Pythagorean combined value 
def logger():
    log.add({
        'x': accelerometer.get_x(),
        'y': accelerometer.get_y(),
        'z': accelerometer.get_z()
    })
```

**Main Loop:**

The script begins by initialising `logging` to be `False`. Then, every 50ms* it will question whether any buttons have been pressed.

> *50ms: assuming unchanged since time of writing; this value may be changed if the log storage fills too quickly.

If <kbd>A</kbd> has been pressed, `logging` is set to `True`. <br>
If <kbd>B</kbd> has been pressed, `logging` is set to `False`. <br>
If <kbd>A</kbd> and <kbd>B</kbd> are pressed, the `clear_log` function is called to delete the log file, `"MY_DATA"`.

If `logging` is set to `True`, the `logger()` function is called. Since this call is within the outer `while True` loop, this function can be called every ~50ms*.
> *50ms delay + Loop Runtime

```py
# Pre initialise 'logging' as False / OFF
logging = False

while True:
    sleep(50) # milliseconds
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
```

### Not Connected Visualiser

**Imports:**

```py
from tkinter import filedialog as fd
import pandas as pd
from matplotlib import pyplot as plt
from scipy import signal
```

**File Selection and Reading:**

Opens a File Explorer window allowing the user to select the `.csv` file to plot. This file is read into a `panda` `Dataframe` Object using a comma `,` as the delimiter. `.reset_index()` creates an `index` column which is used as the x-variable during plotting.
```py
file = fd.askopenfilename(
    filetypes=[("CSV files", "*.csv")],title="Set input .csv file" )

data = pd.read_csv(file, header=0, delimiter=",").reset_index()
```

**Plot Data:**

Plot `Time` against `x`, `y`, `z` and `strength`. Assign each property its own colour and `label`.
```py
plt.plot(data["Time (seconds)"], data.x, "r", label="X")
plt.plot(data["Time (seconds)"], data.y, "g", label="Y")
plt.plot(data["Time (seconds)"], data.z, "b", label="Z")
```

**Format the Plot:**

```py
plt.title("micro:bit Data Logger")
plt.ylabel("Magnitude")
plt.ylim(-1500, 1500)
plt.legend()
```

**Plot Peaks:**

Plot vertical lines at signal peaks; sudden movements.
```py
peaks, props = signal.find_peaks(data.strength, threshold=150)
for peak in peaks:
    plt.axvline(peak, color="k")
```

### Not Connected Visualiser 3D

**Imports:**

```py
from tkinter import filedialog as fd
import pandas as pd
import matplotlib.pyplot as plt
```

**File Selection and Reading:**

Opens a File Explorer window allowing the user to select the `.csv` file to plot. This file is read into a `panda` `Dataframe` Object using a comma `,` as the delimiter. `.reset_index()` creates an `index` column which is used as the x-variable during plotting.
```py
file = fd.askopenfilename(
    filetypes=[("CSV files", "*.csv")],title="Set input .csv file" )

data = pd.read_csv(file, header=0, delimiter=",")
```

This line assigns in parallel the columns from `data` to their own variables. It is not entirely necessary but does *slightly* improve readability.
```py
x, y, z = data.x, data.y, data.z
```

**Create 3D Plot:**

Create the figure `fig` and 3D axis `ax`. Plot the data as a continuous line showing the movement of the micro:bit.
```py
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x, y, z, color='k')

ax.set_xlim(-1500, 1500)
ax.set_ylim(-1500, 1500)
ax.set_zlim(-1500, 1500)

plt.show()
```

---

## Flashing to micro:bit

[Python micro:bit Web Editor](https://python.microbit.org/v/3)

Click `Send to micro:bit`.

![](/README_assets/1_web_editor.jpg)

Follow instructions on screen.

![](/README_assets/2_connect__cable.jpg)

Connect to micro:bit.

![](/README_assets/3_popup.jpg)

---

## Output

### Serial Port Connection

![connected-2d](/README_assets/connected_2d.gif)
![connected-3d](/README_assets/connected_3d.gif)

### From CSV Data

![csv-2d](/README_assets/file_2d.gif)
![csv-3d](/README_assets/file_3d.gif)