from tkinter import filedialog as fd
import pandas as pd
from matplotlib import pyplot as plt
from scipy import signal

file = fd.askopenfilename(
    filetypes=[("CSV files", "*.csv")],title="Set input .csv file" )

data = pd.read_csv(file, header=0, delimiter=",").reset_index()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(data.index, data.x, "r", label="X")
ax.plot(data.index, data.y, "g", label="Y")
ax.plot(data.index, data.z, "b", label="Z")

plt.title("micro:bit Data Logger")
plt.ylabel("Magnitude")
plt.ylim(-1500, 1500)
plt.legend()

peaks, props = signal.find_peaks(data.strength, threshold=150)
for peak in peaks:
    plt.axvline(peak, color="k")

plt.show()
