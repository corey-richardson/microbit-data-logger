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

# Create the figure to plot to
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Plot the data
ax.plot(data.index, data.x, "r", label="X")
ax.plot(data.index, data.y, "g", label="Y")
ax.plot(data.index, data.z, "b", label="Z")

# Set title, ylabel, y-axis bound limits
# Define a legend
plt.title("micro:bit Data Logger")
plt.ylabel("Magnitude")
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
