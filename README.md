# Data Logger Project

---

## Contents

- [aims](#aims)
- [concerns](#concerns)
- [relevant-practice-projects](#relevant-practice-projects)
- [flashing-to-microbit-using-web-based-text-editor](#flashing-to-microbit-using-web-based-text-editor)
<br><br>

Data Logging Visualisation via Serial Port
- [visualing-the-microbit-data-via-usb-cable](#visualing-the-microbit-data-via-usb-cable)
    - [serial-port-writer-mainpy](#serial-port-writer-mainpy)
    - [serial-port-reader-and-realtime-visualiser](#serial-port-reader-and-realtime-visualiser)
    - [serial-port-reader-and-3d-realtime-visualiser](#serial-port-reader-and-3d-realtime-visualiser)
<br><br>

Data Logging Visualisation via CSV Files
- [visualing-the-microbit-with-csv-data](#visualing-the-microbit-with-csv-data)
    - [process](#process)
    - [csv-data-writer-mainpy](#csv-data-writer-mainpy)
    - [csv-data-visualiser](#csv-data-visualiser)
    - [csv-data-3d-visualiser](#csv-data-3d-visualiser)
<br><br>

Output GIFS
- [output](#output)
    - [serial-port-connection](#serial-port-connection)
    - [from-csv-data](#from-csv-data)
<br><br>

Final Project and Presentation - Archery Data Logger
- [final-project-and-presentation](#final-project-and-presentation)
    - [project-selection](#project-selection)
    - [why](#why)
    - [what-went-well](#what-went-well)
    - [lessons-learned](#lessons-learned)
    - [testing-and-results](#testing-and-results)
    - [potential-application](#potential-application)

---

## Aims

- Find the process of flashing software to the BBC micro:bit
- Use one of the micro:bit practice projects to familarise myself with the micro:bit capabilities and process; [data-logging-project](https://microbit.org/get-started/user-guide/data-logging/)
- Use Python scripts to output the data as graphs.
    - This could be done as a realtime data logger or as plots taken from `.csv` data.
- Create a presentation on a "commercial product" using the micro:bit, writing about the following stages:
    - Project Selection
    - Why?
    - What Went Well
    - Lessons Learned
    - Testing and Results
    - Potential Application
> This could be used by the students as an example of what their presentations should consist of.
- All the while, thnk of how this could be tailored to students of varying experience levels and interests.
    - MakeCode Blocks vs Python
    - How could it be linked to their interests?

---

## Concerns

- [x] Is micro:bit storage non-volatile? *(Will the logs be erased when it is unplugged from power?)*
> Data is stored on your micro:bit even when the power is disconnected. It's easy to access - no software is needed. Plug your micro:bit in to a computer, look in the MICROBIT drive and double-click the MY_DATA file to open it in a web browser.

- [x] Does the micro:bit have enough storage space to record data for the time frames I'm hoping to record?
> Memory: 128 KB. Flash space: 512 KB.

- [x] Can I install Pip / PyPI Modules on a work laptop?
    > :x: Pip / PyPI cannot be used to install Python packages on a work laptop. A different idea would be to supply the students with an executable version of the various plotting scripts. These `.exe` files could be created with [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/). 
    - I believe I have all dependencies other than `PySerial` installed, would a USB transfer from an external device be possible?

- [x] Need to verify if micro:bit will work on work laptop.
    > :red_circle: Works with USB R/W permissions, not with Read Only Permissions. May have to use non-networked laptops OR the BBC micro:bit app.

---

## Relevant Practice Projects

- [micro:bit Projects](https://microbit.org/projects/make-it-code-it/)
- [Meet your micro:bit](https://microbit.org/projects/make-it-code-it/meet-your-microbit/?editor=python)
- [MakeCode Data Logger](https://microbit.org/projects/make-it-code-it/makecode-wireless-data-logger/)
- [Python Data Logger](https://microbit.org/projects/make-it-code-it/python-wireless-data-logger/)
- [Max-Min Temperature Logger](https://microbit.org/projects/make-it-code-it/max-min-thermometer/?editor=makecode)

---

## Flashing to micro:bit using Web Based Text Editor

[Python micro:bit Web Editor](https://python.microbit.org/v/3)

Click `Send to micro:bit`.

![](/README_assets/1_web_editor.jpg)

Follow instructions on screen.

![](/README_assets/2_connect__cable.jpg)

Connect to micro:bit.

![](/README_assets/3_popup.jpg)

---

## Visualing the micro:bit Data via USB Cable

### Serial Port Writer main.py

This script is flashed onto the BBC micro:bit

```py
from microbit import *

while True:
    sleep(50) # milliseconds
    print(accelerometer.get_values())
```

The `print` command outputs to the USB serial port to be picked up by the connected laptop or computer.

### Serial Port Reader and Realtime Visualiser

**Imports:** 

```py
from matplotlib import pyplot as plt
from matplotlib import animation
import serial
```

**Configuration:**

These constants define the serial port to attempt a connection to, the [Baud Rate](https://en.wikipedia.org/wiki/Baud) of the board, the timeout bit, the number of datapoints to display at a time and the rate at which the plot will update.

$$\text{LIMIT} \times \text{RATE} = \text{Number of Seconds Displayed}$$

*The Baud Rate to use can be found or changed in the Device Manager.*

![device--manager](/README_assets/device_manager.jpg)

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

### Serial Port Reader and 3D Realtime Visualiser

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

    ax.plot3D([-1500, 1500], [0, 0], [0, 0], "k--", alpha=0.5)
    ax.plot3D([0, 0], [-1500, 1500], [0, 0], "k--", alpha=0.5)
    ax.plot3D([0, 0], [0, 0], [-1500, 1500], "k--", alpha=0.5)
        
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

## Visualing the micro:bit with CSV Data

### Process

1. Run the data logger via battery power.
2. When you use the data logging feature on the micro:bit V2, an HTML file is created on the `MICROBIT` drive called `MY_DATA` that lets you interact with the logged data.
3. View `MY_DATA` in your browser. The page displays a set of buttons to interact with the data and a table containing the data that has been logged so far.
4. Click the <kbd>Download</kbd> button. This downloads the data in `.csv` format using a period `.` as the delimiter.
5. Run the `/not_connected/visualiser.py` script and follow any instructions that appear on screen.

### CSV Data Writer main.py

**Imports:**

```py
from microbit import *
import log, os
```

**Initialise the columns to log to:**

```py
# Set up columns for logging
log.set_labels('x', 'y', 'z')
```

**Define the `logger` function:**

This is the function that records the `x`, `y` and `z` values from the accelerometer into `"MY_DATA.HTM"`.
```py
# Record the x, y, z values
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

If `logging` is set to `True`, the `logger()` function is called. Since this call is within the outer `while True` loop, this function can be called every ~50ms*.
> *50ms delay + Loop Runtime

```py
# Pre initialise 'logging' as False / OFF
logging = False

while True:
    sleep(50) # milliseconds
    # On "A" button pressed...
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

### CSV Data Visualiser

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

### CSV Data 3D Visualiser

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

ax.plot3D([-1500, 1500], [0, 0], [0, 0], "k--", alpha=0.5)
ax.plot3D([0, 0], [-1500, 1500], [0, 0], "k--", alpha=0.5)
ax.plot3D([0, 0], [0, 0], [-1500, 1500], "k--", alpha=0.5)

plt.show()
```

---

## Output

### Serial Port Connection

![connected-2d](/README_assets/connected_2d.gif)
![connected-3d](/README_assets/connected_3d.gif)

### From CSV Data

![csv-2d](/README_assets/file_2d.gif)
![csv-3d](/README_assets/file_3d.gif)
![csv-3d-with-ref-lines](/README_assets/not_connected_3d.png)

---

## Final Project and Presentation

An interesting scenario to record could be archery. This would show how movement / stabilisation changes throughout the shot process and the vibrations and forces involved during the loose of an arrow. This would be similar to a commercial product called the "Mantis X8 Archery Training Tool for Marksmanship" which measures shot feedback, allowing the archer to visualise movements that the human eye will not see.

### Project Selection

### Why?

### What Went Well

### Lessons Learned

### Testing and Results

### Potential Application

---