from tkinter import filedialog as fd
import pandas as pd
from matplotlib import pyplot as plt
from scipy import signal

file = fd.askopenfilename(
    filetypes=[("CSV files", "*.csv")],title="Set input .csv file" )

data = pd.read_csv(file, delimiter=".")

# Get maximum magnitude + 10% for use as y limit
max_x, max_y, max_z = max(data.x), max(data.y), max(data.z)
min_x, min_y, min_z = min(data.x), min(data.y), min(data.z)
min_x, min_y, min_z = abs(min_x), abs(min_y), abs(min_z)
max_strength, min_strength = max(data.strength), min(data.strength)
limit = max(max_x, max_y, max_z, min_x, min_y, min_z, max_strength, min_strength)
limit *= 1.1

plt.plot(data["Time (seconds)"], data.x, "r", label="X")
plt.plot(data["Time (seconds)"], data.y, "g", label="Y")
plt.plot(data["Time (seconds)"], data.z, "b", label="Z")

plt.plot(data["Time (seconds)"], data.strength, "k", label="strength")

plt.title("micro:bit Data Logger")
plt.ylabel("Magnitude")
plt.ylim(-limit, limit)
plt.legend()

peaks = signal.find_peaks(data.strength)
print(peaks)

# for peak in peaks:
#   plt.axvline(x = peak, color = 'pink')

plt.show()