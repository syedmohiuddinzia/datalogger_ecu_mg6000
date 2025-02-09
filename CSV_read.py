import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Read the data
df = pd.read_csv('28jan2025_data.csv')

# Convert seconds to timedelta and format as a string (HH:MM:SS)
df['Time'] = pd.to_timedelta(df['Seconds'], unit='s').astype(str).str.slice(start=7)  # Keep only HH:MM:SS
df = df[df['Time'] >= '00:08:32']

# Plotting the data
plt.figure(figsize=(12, 6))

# Use the 'Time' column for the x-axis
# plt.plot(df['Time'], df['Throttle Position (%)'], label='Throttle %', color='blue')
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


# import matplotlib.pyplot as plt
# from matplotlib.ticker import MaxNLocator

# # List of variables to plot
# variables_to_plot = [
#     'Engine Status Ready', 'Engine Status Crank',
#     'Engine Status StartW', 'Engine Status Warmup',
#     'Engine Status TPSAEN', 'Engine Status TPSDEN'
# ]

# # Number of variables to plot
# num_vars = len(variables_to_plot)

# # Create subplots
# fig, axes = plt.subplots(num_vars, 1, figsize=(12, 6 * num_vars), sharex=True)

# # Plot each variable in a separate subplot
# for i, var in enumerate(variables_to_plot):
#     axes[i].plot(df['Time'], df[var], label=f"{var} Over Time", color='blue')
#     axes[i].set_title(var, fontsize=14)
#     axes[i].grid(True)
#     axes[i].legend(fontsize=10, loc='upper left')
#     axes[i].set_ylim(0, 1)  # Set y-axis limits between 0 and 1

#     # Limit x-axis ticks to reduce overcrowding
#     axes[i].xaxis.set_major_locator(MaxNLocator(nbins=6))  # Show 6 major x-ticks

# # Set common labels
# fig.text(0.5, 0.04, 'Time (HH:MM:SS)', ha='center', fontsize=14)  # X-axis label
# fig.text(0.04, 0.5, 'Parameters (0 to 1)', va='center', rotation='vertical', fontsize=14)  # Y-axis label

# # Rotate x-axis labels for readability
# for ax in axes:
#     ax.tick_params(axis='x', rotation=45)

# # Adjust layout to prevent overlap
# plt.tight_layout(rect=[0.05, 0.05, 1, 0.95])  # Adjust layout for axis labels

# # Show the plots
# plt.show()
