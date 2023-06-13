# Filedialog opens a File Explorer Window, allowing the user to select the 
# CSV Data to read into a dataframe.
from tkinter import filedialog as fd
# Pandas provides dataframe management
import pandas as pd
# matplotlib.pyplot is used to create graphical visualisations of the data
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
# Signal Processing - find peaks in data
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
gs = GridSpec(9, 6, figure=fig)
# Create axis for raw data and combined delta plot
ax = fig.add_subplot(gs[0:3, 0:3])
d_ax = fig.add_subplot(gs[0:3, 3:6])
# Create axis for seperated delta plots
dx_ax = fig.add_subplot(gs[3:6, 0:2])
dy_ax = fig.add_subplot(gs[3:6, 2:4])
dz_ax = fig.add_subplot(gs[3:6, 4:6])
# Create axis for cropped-in peak plots
xpeak_ax = fig.add_subplot(gs[6:9, 0:2])
ypeak_ax = fig.add_subplot(gs[6:9, 2:4])
zpeak_ax = fig.add_subplot(gs[6:9, 4:6])

fig.tight_layout(pad=2.5)

# Draw horizontal axis reference lines at y=0 on each plot
ax.axhline(0, color="k")
d_ax.axhline(0, color="k")
dx_ax.axhline(0, color="k")
dy_ax.axhline(0, color="k")
dz_ax.axhline(0, color="k")
xpeak_ax.axhline(0, color="k")
ypeak_ax.axhline(0, color="k")
zpeak_ax.axhline(0, color="k")

# Calculate the rolling average of the data.
# This smoothens the data to account for noise.
ROLLER = 4
ALPHA = 0.3
rolling = data.rolling(ROLLER).mean()
rolling = rolling.dropna().reset_index()

# Plot the data - pure
ax.plot(data.index, data.x, "r--", label="X", alpha=ALPHA)
ax.plot(data.index, data.y, "g--", label="Y", alpha=ALPHA)
ax.plot(data.index, data.z, "b--", label="Z", alpha=ALPHA)
# Plot the data - rolling averaged
ax.plot(rolling.index + ROLLER/2, rolling.x, "r", label="X")
ax.plot(rolling.index + ROLLER/2, rolling.y, "g", label="Y")
ax.plot(rolling.index + ROLLER/2, rolling.z, "b", label="Z")

# Calculate the deltas - pure
data['dx'] = data['x'] - data['x'].shift(-1)
data['dy'] = data['y'] - data['y'].shift(-1)
data['dz'] = data['z'] - data['z'].shift(-1)
# Calculate the deltas - rolling averaged
rolling['dx'] = rolling['x'] - rolling['x'].shift(-1)
rolling['dy'] = rolling['y'] - rolling['y'].shift(-1)
rolling['dz'] = rolling['z'] - rolling['z'].shift(-1)

# Plot the deltas - pure
d_ax.plot(data.index, data.dx, "r--", label="X", alpha=ALPHA)
d_ax.plot(data.index, data.dy, "g--", label="Y", alpha=ALPHA)
d_ax.plot(data.index, data.dz, "b--", label="Z", alpha=ALPHA)
# Plot the deltas - rolling averaged
d_ax.plot(rolling.index + ROLLER/2, rolling.dx, "r", label="X")
d_ax.plot(rolling.index + ROLLER/2, rolling.dy, "g", label="Y")
d_ax.plot(rolling.index + ROLLER/2, rolling.dz, "b", label="Z")

# Plot the deltas on seperated axis - pure 
dx_ax.plot(data.index, data.dx, "r--", label="X", alpha=ALPHA)
dy_ax.plot(data.index, data.dy, "g--", label="Y", alpha=ALPHA)
dz_ax.plot(data.index, data.dz, "b--", label="Z", alpha=ALPHA)
# Plot the deltas on seperated axis - rolling averaged 
dx_ax.plot(rolling.index + ROLLER/2, rolling.dx, "r", label="X")
dy_ax.plot(rolling.index + ROLLER/2, rolling.dy, "g", label="Y")
dz_ax.plot(rolling.index + ROLLER/2, rolling.dz, "b", label="Z")

# Plot the deltas on seperated axis - pure
# These will be cropped in to only display the peak
xpeak_ax.plot(data.index, data.dx, "r--", label="X", alpha=ALPHA)
ypeak_ax.plot(data.index, data.dy, "g--", label="Y", alpha=ALPHA)
zpeak_ax.plot(data.index, data.dz, "b--", label="Z", alpha=ALPHA)
# Plot the deltas on seperated axis - rolling averaged
# These will be cropped in to only display the peak
xpeak_ax.plot(rolling.index + ROLLER/2, rolling.dx, "r", label="X")
ypeak_ax.plot(rolling.index + ROLLER/2, rolling.dy, "g", label="Y")
zpeak_ax.plot(rolling.index + ROLLER/2, rolling.dz, "b", label="Z")

# Find max x, y, z magnitude for rolling data, then +50% as leeway
ax_bound = abs( rolling[["x","y","z"]] ).max().max() * 1.5
ax.set_ylim(-ax_bound, ax_bound)
# Find max x, y, z magnitude for rolling deltas, then +50% as leeway
d_bound = abs( rolling[["dx","dy","dz"]] ).max().max() * 1.5
d_ax.set_ylim(-d_bound, d_bound)
# Find max x, y, z magnitude for rolling deltas, then +10% as leeway
peak_bound = abs( rolling[["dx","dy","dz"]] ).max().max() * 1.1

# Set titles and create legends
# Main figure title
fig.suptitle("micro:bit Data Logger")
# Titles for data and deltas
ax.set_title("Raw Data")
d_ax.set_title("Deltas")
# Titles for seperated delta plots
dx_ax.set_title("dx")
dy_ax.set_title("dy")
dz_ax.set_title("dz")
# Titles for seperated peak plots
xpeak_ax.set_title("x_peaks")
ypeak_ax.set_title("y_peaks")
zpeak_ax.set_title("z_peaks")

# Set the upper and lower y limits for the seperated delta plots
dx_ax.set_ylim(-d_bound, d_bound)
dy_ax.set_ylim(-d_bound, d_bound)
dz_ax.set_ylim(-d_bound, d_bound)

# Define legends for the data and delta plots
ax.legend()
d_ax.legend()

# Find where there are peaks in the data
THRESHOLD = 200
x_peaks, x_props = signal.find_peaks(rolling.dx, threshold=THRESHOLD)
y_peaks, y_props = signal.find_peaks(rolling.dy, threshold=THRESHOLD)
z_peaks, z_props = signal.find_peaks(rolling.dz, threshold=THRESHOLD)

# This function plots vertical lines on each of the seperated delta plots to 
# indicate which section of the data is being cropped into on 
# the proceeding plot.
def plot_peaks(axis, peaks):
    axis.axvline(peaks[0] - 20, color="k", alpha=0.7)
    axis.axvline(peaks[0] + 20, color="k", alpha=0.7)
# Call function for each axis 
plot_peaks(dx_ax, x_peaks)
plot_peaks(dy_ax, y_peaks)
plot_peaks(dz_ax, z_peaks)

# Set the x and y bounds for each of the peak plots
xpeak_ax.set_xlim(x_peaks[len(x_peaks)//2] - 20, x_peaks[len(x_peaks)//2] + 20)
xpeak_ax.set_ylim(-peak_bound, peak_bound)

ypeak_ax.set_xlim(y_peaks[len(y_peaks)//2] - 20, y_peaks[len(y_peaks)//2] + 20)
ypeak_ax.set_ylim(-peak_bound, peak_bound)

zpeak_ax.set_xlim(z_peaks[len(z_peaks)//2] - 20, z_peaks[len(z_peaks)//2] + 20)
zpeak_ax.set_ylim(-peak_bound, peak_bound)

# Finally, display the figure
plt.show()
