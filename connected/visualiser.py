from matplotlib import pyplot as plt
from matplotlib import animation
import serial

# Windows Device Manager > Ports (COM & LPT) > "mbed Serial Port"
PORT = 'COM3'
BAUD_RATE = 115_200 # ENSURE THIS MATCHES VALUE IN DEVICE MANAGER
STOP = 1

LIMIT = 75
RATE = 5 # ms

ser = serial.Serial(PORT, BAUD_RATE, timeout=STOP)
ser.close()
ser.open()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

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
        ax.plot(idx, xs, label="X")
        ax.plot(idx, ys, label="Y")
        ax.plot(idx, zs, label="Z")
        
    ax.set_ylim(-1500, 1500)
    plt.title("micro:bit Data Logger")
    plt.ylabel("Magnitude")
        
ani = animation.FuncAnimation(
    fig, 
    animate, fargs=(xs, ys, zs), 
    interval=RATE )

plt.show()

try:
    pass
except KeyboardInterrupt:
    ser.close()
