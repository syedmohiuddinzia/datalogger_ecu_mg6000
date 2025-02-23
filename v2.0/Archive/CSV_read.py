import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
from datetime import datetime

# Define column names explicitly
column_names = [
    "Seconds", "Injection Pulse Width 1 (us)", "Injection Pulse Width 2 (us)", "RPM", "Ignition Advance Angle (deg)",
    "Injection Event Scheduling", "Engine Status Ready", "Engine Status Crank", "Engine Status StartW",
    "Engine Status Warmup", "Engine Status TPSAEN", "Engine Status TPSDEN", "Air-Fuel Ratio Target 1", "Air-Fuel Ratio Target 2",
    "WBO2 Enabled 1", "WBO2 Enabled 2", "Barometric Pressure (kPa)", "Manifold Absolute Pressure (kPa)",
    "Manifold Air Temperature (deg C)", "Cylinder Temperature (deg C)", "Throttle Position (%)", "Battery Voltage (V)"
]

# Read the data with predefined column names
df = pd.read_csv('DataLogger_V2.0/data-20feb25/output_2.csv', names=column_names, header=0)

# Convert seconds to timedelta and format as a string (HH:MM:SS)
df['Time'] = pd.to_timedelta(df['Seconds'], unit='s').astype(str).str.slice(start=7)  # Keep only HH:MM:SS

# Convert pressure values to MPa
df['Barometric Pressure (kPa)'] = df['Barometric Pressure (kPa)'] / 1000
df['Manifold Absolute Pressure (kPa)'] = df['Manifold Absolute Pressure (kPa)'] / 1000

# Create a folder with the current timestamp
current_directory = os.getcwd()
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_folder = os.path.abspath(os.path.join(current_directory, timestamp))

# Ensure the folder is created
os.makedirs(output_folder, exist_ok=True)
print(f"Folder created: {output_folder}")

# Function to create and save plots
def save_plot(x, y_data, labels, colors, xlabel, ylabel, title, filename):
    try:
        plt.figure(figsize=(20, 10))
        for y, label, color in zip(y_data, labels, colors):
            plt.plot(x, y, label=label, color=color, linewidth=0.7)  # Set thinner lines

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.grid(True)

        ax = plt.gca()
        ax.xaxis.set_major_locator(MaxNLocator(nbins=10))
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot
        plot_path = os.path.join(output_folder, filename)
        plt.savefig(plot_path)
        print(f"✅ Saved: {plot_path}")
        plt.close()

    except Exception as e:
        print(f"❌ Error saving {filename}: {e}")

# 1. Injection Pulse Width Plot
save_plot(df['Time'], [df['Injection Pulse Width 1 (us)'], df['Injection Pulse Width 2 (us)']],
          ['Injection Pulse Width 1', 'Injection Pulse Width 2'], ['red', 'blue'],
          'Time', 'Pulse Width (us)', 'Injection Pulse Width Over Time', "injection_pulse_width.png")

# 2. RPM and Throttle Position Plot
save_plot(df['Time'], [df['RPM']],
          ['RPM'], ['red'],
          'Time', 'RPM', 'RPM Time', "rpm.png")

# 3. RPM and Throttle Position Plot
save_plot(df['Time'], [df['Throttle Position (%)']],
          ['Throttle Position %'], ['red'],
          'Time', 'Throttle Position %', 'Throttle Position % over Time', "throttle_position.png")

# 4. Ignition Advance Angle Plot
save_plot(df['Time'], [df['Ignition Advance Angle (deg)']],
          ['Ignition Advance Angle'], ['green'],
          'Time', 'Degrees', 'Ignition Advance Angle Over Time', "ignition_advance.png")

# 5. Injection Event Scheduling Plot
save_plot(df['Time'], [df['Injection Event Scheduling']],
          ['Injection Event Scheduling'], ['black'],
          'Time', 'Injection Event Scheduling', 'Injection Event Scheduling Over Time', "injection_event.png")

# 6. Air-Fuel Ratio Target Plot
save_plot(df['Time'], [df['Air-Fuel Ratio Target 1'], df['Air-Fuel Ratio Target 2']],
          ['AFR Target 1', 'AFR Target 2'], ['green', 'blue'],
          'Time', 'Air-Fuel Ratio', 'Air-Fuel Ratio Targets Over Time', "afr_target.png")

# 7. WBO Enabled Plot
save_plot(df['Time'], [df['WBO2 Enabled 1'], df['WBO2 Enabled 2']],
          ['WBO2 Enabled 1', 'WBO2 Enabled 2'], ['red', 'blue'],
          'Time', 'WBO Status', 'WBO Enabled Over Time', "wbo_enabled.png")

# 8. Barometric and Manifold Pressure Plot
save_plot(df['Time'], [df['Barometric Pressure (kPa)'], df['Manifold Absolute Pressure (kPa)']],
          ['Barometric Pressure (MPa)', 'Manifold Pressure (MPa)'], ['red', 'blue'],
          'Time', 'Pressure (MPa)', 'Barometric and Manifold Pressure Over Time', "pressure.png")

# 9. Temperature Plot (Manifold & Cylinder)
save_plot(df['Time'], [df['Manifold Air Temperature (deg C)'], df['Cylinder Temperature (deg C)']],
          ['Manifold Air Temperature', 'Cylinder Temperature'], ['green', 'blue'],
          'Time', 'Temperature (°C)', 'Manifold and Cylinder Temperature Over Time', "temperature.png")

# 10. Battery Voltage Plot
save_plot(df['Time'], [df['Battery Voltage (V)']],
          ['Battery Voltage'], ['black'],
          'Time', 'Voltage (V)', 'Battery Voltage Over Time', "battery_voltage.png")
