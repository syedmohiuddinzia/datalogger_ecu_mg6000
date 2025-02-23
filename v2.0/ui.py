import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import csv

# Configure matplotlib to use non-GUI backend
plt.switch_backend('Agg')

class DataLoggerApp:
    def __init__(self, master):
        self.master = master
        master.title("Data Logger Processor")
        
        # UI Elements
        self.frame = tk.Frame(master, padx=20, pady=20)
        self.frame.pack()
        
        self.btn_select = tk.Button(self.frame, text="Select Input TXT File", command=self.select_file)
        self.btn_select.pack(pady=10)
        
        self.status_label = tk.Label(self.frame, text="Status: Ready")
        self.status_label.pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select Input TXT File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.process_file(file_path)

    def process_file(self, input_path):
        try:
            self.update_status("Processing: Step 1/3 - Formatting bytes...")
            txt_output = self.process_line82bytes(input_path)
            
            self.update_status("Processing: Step 2/3 - Decrypting CSV...")
            csv_output = self.process_decrypt_csv(txt_output)
            
            self.update_status("Processing: Step 3/3 - Generating plots...")
            self.process_csv_reader(csv_output)
            
            self.update_status("Processing complete!")
            messagebox.showinfo("Success", "Processing completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Error occurred")

    def process_line82bytes(self, input_file):
        output_file = os.path.join(os.path.dirname(input_file), "processed_data.txt")
        with open(input_file, "r") as f:
            data = f.read().split()
        
        chunks = [data[i:i+82] for i in range(0, len(data), 82)]
        
        with open(output_file, "w") as f:
            for chunk in chunks:
                if len(chunk) != 82:
                    print(f"Warning: Skipping line with {len(chunk)} values")
                    continue
                
                # Modified filtering logic
                if chunk[0] != "00" and chunk[0] != "f0" :  # Keep lines with pattern "XX 00"
                    if chunk[2] != "00":
                        f.write(" ".join(chunk) + "\n")
                        # print(f"Kept valid line: {chunk[0]} {chunk[1]}...")
                # else:
                    # print(f"Removed garbage line: {chunk[0]} {chunk[1]}...")

        return output_file

    def process_decrypt_csv(self, input_txt):
        output_csv = os.path.join(os.path.dirname(input_txt), "decrypted_data.csv")
        parsed_data = []
        
        with open(input_txt, 'r') as f:
            for line in f:
                result = self.parse_data_line(line)
                if result:
                    parsed_data.append(result[1])
        
        # Define CSV headers
        headers = [
            "Seconds", "Injection Pulse Width 1 (us)", "Injection Pulse Width 2 (us)",
            "RPM", "Ignition Advance Angle (deg)", "Injection Event Scheduling",
            "Engine Status Ready", "Engine Status Crank", "Engine Status StartW",
            "Engine Status Warmup", "Engine Status TPSAEN", "Engine Status TPSDEN",
            "Air-Fuel Ratio Target 1", "Air-Fuel Ratio Target 2", "WBO2 Enabled 1",
            "WBO2 Enabled 2", "Barometric Pressure (kPa)", "Manifold Absolute Pressure (kPa)",
            "Manifold Air Temperature (deg C)", "Cylinder Temperature (deg C)",
            "Throttle Position (%)", "Battery Voltage (V)"
        ]
        
        with open(output_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(parsed_data)
        
        return output_csv

    def parse_data_line(self, line):
        # Helper functions from decryptCSV
        def fahrenheit_to_celsius(f):
            return (f - 32) * 5 / 9

        def shift_and_combine(h, l):
            return (int(h, 16) << 8) | int(l, 16)

        def shift_and_combine_signed(h, l):
            combined = (int(h, 16) << 8) | int(l, 16)
            return combined - 0x10000 if combined >= 0x8000 else combined

        # Parsing logic
        try:
            hex_values = [v.zfill(2) for v in line.strip().split()]
            
            # Convert various values
            seconds = shift_and_combine(hex_values[1], hex_values[0])
            pw1 = shift_and_combine(hex_values[3], hex_values[2])
            pw2 = shift_and_combine(hex_values[5], hex_values[4])
            rpm = shift_and_combine(hex_values[7], hex_values[6])
            adv_deg = shift_and_combine(hex_values[9], hex_values[8]) / 10
            baro = shift_and_combine_signed(hex_values[17], hex_values[16]) / 10
            map_ = shift_and_combine_signed(hex_values[19], hex_values[18]) / 10
            mat = fahrenheit_to_celsius(shift_and_combine_signed(hex_values[21], hex_values[20]) / 10)
            clt = fahrenheit_to_celsius(shift_and_combine_signed(hex_values[23], hex_values[22]) / 10)
            tps = shift_and_combine_signed(hex_values[25], hex_values[24]) / 10
            batt = shift_and_combine_signed(hex_values[27], hex_values[26]) / 10
            
            # Engine status parsing
            engine = int(hex_values[11], 16)
            engine_status = [
                bool(engine & (1 << i)) for i in range(6)
            ]
            
            return (None, [
                seconds, pw1, pw2, rpm, adv_deg, int(hex_values[10], 16),
                *engine_status,
                int(hex_values[12], 16), int(hex_values[13], 16),
                int(hex_values[14], 16), int(hex_values[15], 16),
                baro, map_, mat, clt, tps, batt
            ])
        except Exception as e:
            print(f"Error parsing line: {e}")
            return None

    def process_csv_reader(self, csv_path):
        # Read and process data
        column_names = [
            "Seconds", "Injection Pulse Width 1 (us)", "Injection Pulse Width 2 (us)", "RPM", 
            "Ignition Advance Angle (deg)", "Injection Event Scheduling", "Engine Status Ready", 
            "Engine Status Crank", "Engine Status StartW", "Engine Status Warmup", "Engine Status TPSAEN", 
            "Engine Status TPSDEN", "Air-Fuel Ratio Target 1", "Air-Fuel Ratio Target 2", 
            "WBO2 Enabled 1", "WBO2 Enabled 2", "Barometric Pressure (kPa)", "Manifold Absolute Pressure (kPa)",
            "Manifold Air Temperature (deg C)", "Cylinder Temperature (deg C)", "Throttle Position (%)", 
            "Battery Voltage (V)"
        ]
        
        df = pd.read_csv(csv_path, names=column_names, header=0)
        df['Time'] = pd.to_timedelta(df['Seconds'], unit='s').astype(str).str.slice(start=7)
        df['Barometric Pressure (kPa)'] /= 1000
        df['Manifold Absolute Pressure (kPa)'] /= 1000
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(csv_path), datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate plots
        self.generate_plots(df, output_dir)

    def generate_plots(self, df, output_dir):
        plots = [
            (['Injection Pulse Width 1 (us)', 'Injection Pulse Width 2 (us)'], ['red', 'blue'], 'Pulse Width (us)', 'injection_pulse_width.png'),
            (['RPM'], ['red'], 'RPM', 'rpm.png'),
            (['Throttle Position (%)'], ['red'], 'Throttle Position %', 'throttle_position.png'),
            (['Ignition Advance Angle (deg)'], ['green'], 'Degrees', 'ignition_advance.png'),            
            (['Injection Event Scheduling'], ['green'], 'Injection Event Scheduling', 'injection_event.png'),
            (['Air-Fuel Ratio Target 1', 'Air-Fuel Ratio Target 2'], ['green', 'blue'], 'Air-Fuel Ratio', 'afr_target.png'),
            (['WBO2 Enabled 1', 'WBO2 Enabled 2'], ['green', 'blue'], 'WBO Status', 'wbo_enabled.png'),
            (['Barometric Pressure (kPa)', 'Manifold Absolute Pressure (kPa)'], ['red', 'blue'], 'Pressure (MPa)', 'pressure.png'),
            (['Manifold Air Temperature (deg C)', 'Cylinder Temperature (deg C)'], ['red', 'blue'], 'Temperature (°C)', 'temperature.png'),
            (['Battery Voltage (V)'], ['green'], 'Voltage (V)', 'battery_voltage.png'),
        ]

        for columns, colors, ylabel, filename in plots:
            plt.figure(figsize=(20, 10))
            for col, color in zip(columns, colors):
                plt.plot(df['Time'], df[col], label=col, color=color, linewidth=0.7)

            plt.xlabel("Time")  
            plt.ylabel(ylabel)
            plt.legend()
            plt.grid(True)

            # Reduce the number of x-axis labels
            plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))  

            plt.xticks(rotation=90)  
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, filename))
            plt.close()


    def update_status(self, message):
        self.status_label.config(text=message)
        self.master.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataLoggerApp(root)
    root.mainloop()