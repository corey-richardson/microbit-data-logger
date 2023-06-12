from tkinter import filedialog as fd
import pandas as pd
import matplotlib.pyplot as plt

file = fd.askopenfilename(
    filetypes=[("CSV files", "*.csv")],title="Set input .csv file" )

data = pd.read_csv(file, header=0, delimiter=",")

x, y, z = data.x, data.y, data.z

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x, y, z)

ax.set_xlim(-1500, 1500)
ax.set_ylim(-1500, 1500)
ax.set_zlim(-1500, 1500)

ax.plot3D([-1500, 1500], [0, 0], [0, 0], "k--", alpha=0.5)
ax.plot3D([0, 0], [-1500, 1500], [0, 0], "k--", alpha=0.5)
ax.plot3D([0, 0], [0, 0], [-1500, 1500], "k--", alpha=0.5)

# # Rotating
# angle = 0
# while True:
#    ax.view_init(30, angle%360)
#    angle+=1
#    plt.draw()
#    plt.pause(.001)

plt.show()
