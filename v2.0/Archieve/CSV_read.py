import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Read the data
df = pd.read_csv('DataLogger_V2.0/data-20feb25/output_1.csv')

# Convert seconds to timedelta and format as a string (HH:MM:SS)
df['Time'] = pd.to_timedelta(df['Seconds'], unit='s').astype(str).str.slice(start=7)  # Keep only HH:MM:SS
# df = df[df['Time'] >= '00:08:32']

# Plotting the data
plt.figure(figsize=(12, 6))

plt.plot(df['Time'], df['RPM'], label='RPM', color='red')
plt.plot(df['Time'], df['Manifold Air Temperature (deg C)'], label='Injection Pulse Width 2 (us)', color='green')

# Set the labels and title
plt.xlabel('Time (HH:MM:SS)')
plt.ylabel('Parameters')
plt.title('ECU Data')

# Show legend and grid
plt.legend()
plt.grid(True)

# Limit the number of x-axis ticks
ax = plt.gca()
ax.xaxis.set_major_locator(MaxNLocator(nbins=10))

# Rotate x-axis labels for readability
plt.xticks(rotation=45)

# Adjust layout to fit the labels
plt.tight_layout()

# Show the plot
plt.show()

