from matplotlib import pyplot as plt
from matplotlib import animation
from numpy import diff
import serial

# Windows Device Manager > Ports (COM & LPT) > "mbed Serial Port"
PORT = 'COM3'
BAUD_RATE = 115_200 # ENSURE THIS MATCHES VALUE IN DEVICE MANAGER
STOP = 1

LIMIT = 25
RATE = 5 # ms

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
    
    d_xs = diff(xs)
    d_ys = diff(ys)
    d_zs = diff(zs)
    
    if len(xs) == LIMIT:
        ax.clear()
        ax.plot3D(xs, ys, zs, label="State")
        ax.plot3D(d_xs, d_ys, d_zs, label="Deltas")
    
    ax.set_xlim(-1500, 1500)
    ax.set_ylim(-1500, 1500)
    ax.set_zlim(-1500, 1500)
    ax.legend()
    
    # ax.set_xlabel("x")
    # ax.set_ylabel("y")
    # ax.set_zlabel("z")
    
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
