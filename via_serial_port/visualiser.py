from matplotlib import pyplot as plt
from matplotlib import animation
import serial
from numpy import diff, arange

# Windows Device Manager > Ports (COM & LPT) > "mbed Serial Port"
PORT = 'COM3'
BAUD_RATE = 115_200 # ENSURE THIS MATCHES VALUE IN DEVICE MANAGER
STOP = 1

LIMIT = 300
RATE = 50 # ms

estimated_timings = range(int(LIMIT//10), 0, -1)

ser = serial.Serial(PORT, BAUD_RATE, timeout=STOP)
ser.close()
ser.open()

fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
d_ax = fig.add_subplot(2, 1, 2)
    
xs, ys, zs = [0]*LIMIT, [0]*LIMIT, [0]*LIMIT

def animate(i, xs, ys, zs):
        
    line = ser.readline().decode("utf-8").strip("(").strip(")\r\n")
    x, y, z = line.split(",")
    x, y, z = int(x), int(y), int(z)
    
    print(x, y, z)
    
    idx = range(LIMIT)
    d_idx = range(LIMIT - 1)
    xs.append(x)
    ys.append(y)
    zs.append(z)
    
    xs = xs[-LIMIT:]
    ys = ys[-LIMIT:]
    zs = zs[-LIMIT:]
    
    d_xs = diff(xs)
    d_ys = diff(ys)
    d_zs = diff(zs)

    if len(xs) == LIMIT:
        ax.clear()
        d_ax.clear()
        
        ax.plot(idx, xs, color="r", label="X")
        ax.plot(idx, ys, color="g", label="Y")
        ax.plot(idx, zs, color="b", label="Z")
        
        d_ax.plot(d_idx, d_xs, color="r")
        d_ax.plot(d_idx, d_ys, color="g")
        d_ax.plot(d_idx, d_zs, color="b")
        d_ax.axhline(0, color="k")
    
    ax.set_ylim(-4500, 4500)
    d_ax.set_ylim(-4500, 4500)

    ax.legend()

    fig.suptitle("micro:bit Data Logger")

    # ax.set_xlabel("Time Since (s)")
    # d_ax.set_xlabel("Time Since (s)")
    # ax.set_xticks(range(0, LIMIT, 10), estimated_timings)
    # d_ax.set_xticks(range(0, LIMIT, 10), estimated_timings)

ani = animation.FuncAnimation(
    fig, 
    animate, fargs=(xs, ys, zs), 
    interval=RATE )

plt.show()

try:
    pass
except KeyboardInterrupt:
    ser.close()
