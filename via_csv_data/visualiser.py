# Filedialog opens a File Explorer Window, allowing the user to select the 
# CSV Data to read into a dataframe.
from tkinter import filedialog as fd
# Pandas provides dataframe management
import pandas as pd
# matplotlib.pyplot is used to create graphical visualisations of the data
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
# scipy.signal is used to show where peaks are in the data
from scipy import signal

# Open file explorer window for user to select CSV Data
file = fd.askopenfilename(
    filetypes=[("CSV files", "*.csv")],title="Set input .csv file" )
# Read the selected data into a dataframe
# .reset_index() creates an index column
data = pd.read_csv(file, header=0).reset_index()

data["time"] = data["Time (seconds)"] - min(data["Time (seconds)"])

# Create the figure to plot to
fig = plt.figure(figsize=(10, 10))
gs = GridSpec(6, 6, figure=fig)
# Create subplots, organised using GridSpec
ax = fig.add_subplot(gs[0:3, 0:3])
d_ax = fig.add_subplot(gs[0:3, 3:6])
dx_ax = fig.add_subplot(gs[3:6, 0:2])
dy_ax = fig.add_subplot(gs[3:6, 2:4])
dz_ax = fig.add_subplot(gs[3:6, 4:6])
fig.tight_layout(pad=2.5)

ax.axhline(0, color="k")
d_ax.axhline(0, color="k")
dx_ax.axhline(0, color="k")
dy_ax.axhline(0, color="k")
dz_ax.axhline(0, color="k")


ROLLER = 4
ALPHA = 0.3
rolling = data.rolling(ROLLER).mean()
rolling = rolling.dropna().reset_index()

# Plot the data
ax.plot(data.index, data.x, "r--", label="X", alpha=ALPHA)
ax.plot(data.index, data.y, "g--", label="Y", alpha=ALPHA)
ax.plot(data.index, data.z, "b--", label="Z", alpha=ALPHA)

ax.plot(rolling.index + ROLLER/2, rolling.x, "r", label="X")
ax.plot(rolling.index + ROLLER/2, rolling.y, "g", label="Y")
ax.plot(rolling.index + ROLLER/2, rolling.z, "b", label="Z")

data['dx'] = data['x'] - data['x'].shift(-1)
data['dy'] = data['y'] - data['y'].shift(-1)
data['dz'] = data['z'] - data['z'].shift(-1)

rolling['dx'] = rolling['x'] - rolling['x'].shift(-1)
rolling['dy'] = rolling['y'] - rolling['y'].shift(-1)
rolling['dz'] = rolling['z'] - rolling['z'].shift(-1)

d_ax.plot(data.index, data.dx, "r--", label="X", alpha=ALPHA)
d_ax.plot(data.index, data.dy, "g--", label="Y", alpha=ALPHA)
d_ax.plot(data.index, data.dz, "b--", label="Z", alpha=ALPHA)

d_ax.plot(rolling.index + ROLLER/2, rolling.dx, "r", label="X")
d_ax.plot(rolling.index + ROLLER/2, rolling.dy, "g", label="Y")
d_ax.plot(rolling.index + ROLLER/2, rolling.dz, "b", label="Z")

dx_ax.plot(data.index, data.dx, "r--", label="X", alpha=ALPHA)
dy_ax.plot(data.index, data.dy, "g--", label="Y", alpha=ALPHA)
dz_ax.plot(data.index, data.dz, "b--", label="Z", alpha=ALPHA)

dx_ax.plot(rolling.index + ROLLER/2, rolling.dx, "r", label="X")
dy_ax.plot(rolling.index + ROLLER/2, rolling.dy, "g", label="Y")
dz_ax.plot(rolling.index + ROLLER/2, rolling.dz, "b", label="Z")

# Find max x, y, z magnitude for rolling data, then +20% as leeway
ax_bound = abs( rolling[["x","y","z"]] ).max().max() * 1.5
ax.set_ylim(-ax_bound, ax_bound)
# Find max x, y, z magnitude for rolling deltas, then +20% as leeway
d_bound = abs( rolling[["dx","dy","dz"]] ).max().max() * 1.5
d_ax.set_ylim(-d_bound, d_bound)

# Set titles and create legends
fig.suptitle("micro:bit Data Logger")
ax.set_title("Raw Data")
d_ax.set_title("Deltas")
dx_ax.set_title("dx")
dy_ax.set_title("dy")
dz_ax.set_title("dz")

dx_ax.set_ylim(-d_bound, d_bound)
dy_ax.set_ylim(-d_bound, d_bound)
dz_ax.set_ylim(-d_bound, d_bound)

ax.legend()
d_ax.legend()

THRESHOLD = 200
x_peaks, x_props = signal.find_peaks(rolling.dx, threshold=THRESHOLD)
y_peaks, y_props = signal.find_peaks(rolling.dy, threshold=THRESHOLD)
z_peaks, z_props = signal.find_peaks(rolling.dz, threshold=THRESHOLD)

def plot_peaks(axis, peaks):
    for peak in peaks:
        axis.axvline(peak, color="k", alpha=0.5)

# plot_peaks(dx_ax, x_peaks)
# plot_peaks(dy_ax, y_peaks)
# plot_peaks(dz_ax, z_peaks)

plt.show()
