from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import style
import numpy as np
import sys
import serial

# Windows Device Manager > Ports (COM & LPT) > "mbed Serial Port"
PORT = 'COM3'
BAUD_RATE = 115_200
STOP = 1

LIMIT = 20
RATE = 50 # ms

# Make connection
ser = serial.Serial(PORT, BAUD_RATE, timeout=STOP)

# Open connection and test if succeeded
try:
    ser.open()
except serial.serialutil.SerialException:
    sys.exit(f"Connection to Serial Port '{PORT}' Failed")
    
if ser.is_open:
    print(f"Port Open on {ser.name}: \n{ser}\n")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

xs, ys, zs = [], [], []

def animate(times, xs, ys, zs):
    # Parse data from Serial port
    line = ser.readline()
    time, x, y, z = line.split('.')
    print(f"{line} PARSED_TO {time}: {x}, {y}, {z}")
    
    # Append new value to list
    times.append(time)
    xs.append(x)
    ys.append(y)
    zs.append(z)
    
    # Limit lists to LIMIT number of items (Removes oldest value)
    times = times[-LIMIT:]
    xs = xs[-LIMIT:]
    ys = ys[-LIMIT:]
    zs = zs[-LIMIT:]
    
    # Draw x, y and z lists
    ax.clear()
    ax.plot(times, xs, label="X")
    ax.plot(times, ys, label="Y")
    ax.plot(times, zs, label="Z")
    
    # Format the plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title("micro:bit Data Logger")
    plt.ylabel("Magnitude")
    plt.legend()
    plt.axis([1, None, 0, 1.1])
    
    

ani = animation.FuncAnimation(
    fig, 
    animate, fargs=(xs, ys, zs), 
    interval=RATE )

plt.show(block=False)
