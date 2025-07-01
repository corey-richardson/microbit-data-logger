# Filedialog opens a File Explorer Window, allowing the user to select the
# CSV Data to read into a dataframe.
from tkinter import filedialog as fd
# Pandas provides dataframe management
import pandas as pd
# matplotlib.pyplot is used to create graphical visualisations of the data
from matplotlib import pyplot as plt

# Open file explorer window for user to select CSV Data
file = fd.askopenfilename(
    filetypes=[("CSV files", "*.csv")], title="Set input .csv file")
# Read the selected data into a dataframe
data = pd.read_csv(file, header=0)

# Create a 3D figure to plot the data on
fig = plt.figure()
ax = plt.axes(projection='3d')

# Plot the data onto the figure
ax.plot3D(data.x, data.y, data.z)

# Set the figures x, y and z bound limits
bound = 1500  # +/-
ax.set_xlim(-bound, bound)
ax.set_ylim(-bound, bound)
ax.set_zlim(-bound, bound)

# Set labels for the x, y and z planes
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

#
ax.plot3D([-bound, bound], [0, 0], [0, 0], "k--", alpha=0.5)
ax.plot3D([0, 0], [-bound, bound], [0, 0], "k--", alpha=0.5)
ax.plot3D([0, 0], [0, 0], [-bound, bound], "k--", alpha=0.5)

# # Rotating
# angle = 0
# while True:
#    ax.view_init(30, angle%360)
#    angle+=1
#    plt.draw()
#    plt.pause(.001)

plt.show()
