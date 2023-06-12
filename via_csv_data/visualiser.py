# Filedialog opens a File Explorer Window, allowing the user to select the 
# CSV Data to read into a dataframe.
from tkinter import filedialog as fd
# Pandas provides dataframe management
import pandas as pd
# matplotlib.pyplot is used to create graphical visualisations of the data
from matplotlib import pyplot as plt

# Open file explorer window for user to select CSV Data
file = fd.askopenfilename(
    filetypes=[("CSV files", "*.csv")],title="Set input .csv file" )
# Read the selected data into a dataframe
# .reset_index() creates an index column
data = pd.read_csv(file, header=0).reset_index()
data.time = data["Time (seconds)"] - min(data["Time (seconds)"])
# Create the figure to plot to
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(2, 1, 1)
d_ax = fig.add_subplot(2, 1, 2)

roller = 5
rolling = data.rolling(roller).mean().dropna()

# Plot the data
ax.plot(data.time, data.x, "r--", label="X", alpha=0.3)
ax.plot(data.time, data.y, "g--", label="Y", alpha=0.3)
ax.plot(data.time, data.z, "b--", label="Z", alpha=0.3)
# Plot the rolling data
ax.plot(data.time[roller-1:], rolling.x, "r", label="X")
ax.plot(data.time[roller-1:], rolling.y, "g", label="Y")
ax.plot(data.time[roller-1:], rolling.z, "b", label="Z")

# Calculate the deltas
data['dx'] = data['x'] - data['x'].shift(-1)
data['dy'] = data['y'] - data['y'].shift(-1)
data['dz'] = data['z'] - data['z'].shift(-1)
# Calculate the rolling deltas
rolling['dx'] = rolling['x'] - rolling['x'].shift(-1)
rolling['dy'] = rolling['y'] - rolling['y'].shift(-1)
rolling['dz'] = rolling['z'] - rolling['z'].shift(-1)

# Plot the deltas
d_ax.plot(data.time, data.dx, "r--", label="X", alpha=0.3)
d_ax.plot(data.time, data.dy, "g--", label="Y", alpha=0.3)
d_ax.plot(data.time, data.dz, "b--", label="Z", alpha=0.3)
# Plot the rolling deltas
d_ax.plot(data.time[roller-1:], rolling.dx, "r", label="X")
d_ax.plot(data.time[roller-1:], rolling.dy, "g", label="Y")
d_ax.plot(data.time[roller-1:], rolling.dz, "b", label="Z")

# Set title, ylabel, y-axis bound limits
# Define a legend
ax.set_title("micro:bit Data Logger")
d_ax.set_title("Deltas")
plt.xlabel("Time (s)")
plt.ylim(-1500, 1500)
plt.legend()

# from scipy import signal

# x_peaks, x_props = signal.find_peaks(data.x, threshold=150)
# y_peaks, y_props = signal.find_peaks(data.x, threshold=150)
# z_peaks, z_props = signal.find_peaks(data.x, threshold=150)
# peaks = x_peaks, y_peaks, z_peaks

# peaks = [x_peaks, y_peaks, z_peaks]

# for n_peaks in peaks:
#     for peaks in n_peaks:
#         print(peaks)
#         plt.axvline(peaks, color="k")
    
plt.show()
