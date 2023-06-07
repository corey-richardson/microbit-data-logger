from tkinter import filedialog as fd
import pandas as pd
import matplotlib.pyplot as plt

file = fd.askopenfilename(
    filetypes=[("CSV files", "*.csv")],title="Set input .csv file" )

data = pd.read_csv(file, delimiter=".")

x, y, z = data.x, data.y, data.z

fig = plt.figure()

ax = plt.axes(projection='3d')
ax.plot3D(x, y, z, color='k')

plt.show()
