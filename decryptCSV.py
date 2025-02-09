import csv

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9

def pad_hex(value):
    """Pad the hex value to ensure it is two digits."""
    return value.zfill(2).upper()

def shift_and_combine(high, low):
    """Shift high value to the left and combine with low value (for uint16)."""
    return (int(high, 16) << 8) | int(low, 16)

def shift_and_combine_signed(high, low):
    """Shift high value to the left and combine with low value (for int16)."""
    combined = (int(high, 16) << 8) | int(low, 16)
    if combined >= 0x8000:
        combined -= 0x10000  # Handle signed 16-bit integers
    return combined

def parse_engine_status(engine_value):
    """Parse the engine status from the 8-bit value (uint8)."""
    engine = int(engine_value, 16)
    return {
        "Ready": (engine & (1 << 0)) != 0,
        "Crank": (engine & (1 << 1)) != 0,
        "StartW": (engine & (1 << 2)) != 0,
        "Warmup": (engine & (1 << 3)) != 0,
        "TPSAEN": (engine & (1 << 4)) != 0,
        "TPSDEN": (engine & (1 << 5)) != 0,
    }

def parse_data_line(line):
    """Parse a single line of data from the log file."""
    hex_values = line.strip().split()
    hex_values = [pad_hex(value) for value in hex_values]

    try:
        # uint16 values
        seconds_hex = f"{hex_values[1]}{hex_values[0]}"
        seconds = shift_and_combine(hex_values[1], hex_values[0])

        pw1_hex = f"{hex_values[3]}{hex_values[2]}"
        pw1 = shift_and_combine(hex_values[3], hex_values[2])

        pw2_hex = f"{hex_values[5]}{hex_values[4]}"
        pw2 = shift_and_combine(hex_values[5], hex_values[4])

        rpm_hex = f"{hex_values[7]}{hex_values[6]}"
        rpm = shift_and_combine(hex_values[7], hex_values[6])

        adv_deg_hex = f"{hex_values[9]}{hex_values[8]}"
        adv_deg = shift_and_combine(hex_values[9], hex_values[8]) / 10

        # int16 values
        baro_hex = f"{hex_values[17]}{hex_values[16]}"
        baro = shift_and_combine_signed(hex_values[17], hex_values[16]) / 10

        map_hex = f"{hex_values[19]}{hex_values[18]}"
        map = shift_and_combine_signed(hex_values[19], hex_values[18]) / 10

        mat_hex = f"{hex_values[21]}{hex_values[20]}"
        mat = fahrenheit_to_celsius(shift_and_combine_signed(hex_values[21], hex_values[20]) / 10)

        clt_hex = f"{hex_values[23]}{hex_values[22]}"
        clt = fahrenheit_to_celsius(shift_and_combine_signed(hex_values[23], hex_values[22]) / 10)

        tps_hex = f"{hex_values[25]}{hex_values[24]}"
        tps = shift_and_combine_signed(hex_values[25], hex_values[24]) / 10

        batt_hex = f"{hex_values[27]}{hex_values[26]}"
        batt = shift_and_combine_signed(hex_values[27], hex_values[26]) / 10

        # uint8 values
        squirt_hex = hex_values[10]
        squirt = int(hex_values[10], 16)

        engine_value_hex = hex_values[11]
        engine_status = parse_engine_status(engine_value_hex)

        afrtgt1_hex = hex_values[12]
        afrtgt1 = int(hex_values[12], 16)

        afrtgt2_hex = hex_values[13]
        afrtgt2 = int(hex_values[13], 16)

        wbo2_en1_hex = hex_values[14]
        wbo2_en1 = int(hex_values[14], 16)

        wbo2_en2_hex = hex_values[15]
        wbo2_en2 = int(hex_values[15], 16)

        return [
            # Hexadecimal values
            [seconds_hex, pw1_hex, pw2_hex, rpm_hex, adv_deg_hex, squirt_hex, engine_value_hex,
            afrtgt1_hex, afrtgt2_hex, wbo2_en1_hex, wbo2_en2_hex, baro_hex, map_hex, mat_hex,
            clt_hex, tps_hex, batt_hex],

            # Decimal values
            [seconds, pw1, pw2, rpm, adv_deg, squirt,
            engine_status["Ready"], engine_status["Crank"], engine_status["StartW"],
            engine_status["Warmup"], engine_status["TPSAEN"], engine_status["TPSDEN"],
            afrtgt1, afrtgt2, wbo2_en1, wbo2_en2, baro, map, mat, clt, tps, batt]
        ]
    except (IndexError, ValueError):
        print(f"Error parsing line: {line}")
        return None

def write_decimal_to_csv(filename, data):
    """Write the decimal values to a CSV file."""
    if not data:
        print("No data to write.")
        return

    fieldnames = [
        "Seconds", "Injection Pulse Width 1 (us)", "Injection Pulse Width 2 (us)",
        "RPM", "Ignition Advance Angle (deg)", "Injection Event Scheduling",
        "Engine Status Ready", "Engine Status Crank", "Engine Status StartW",
        "Engine Status Warmup", "Engine Status TPSAEN", "Engine Status TPSDEN",
        "Air-Fuel Ratio Target 1", "Air-Fuel Ratio Target 2", "WBO2 Enabled 1",
        "WBO2 Enabled 2", "Barometric Pressure (kPa)", "Manifold Absolute Pressure (kPa)",
        "Manifold Air Temperature (deg C)", "Cylinder Temperature (deg C)",
        "Throttle Position (%)", "Battery Voltage (V)"
    ]

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(dict(zip(fieldnames, row)))

def print_all_hex(parsed_data_list):
    """Print all the hexadecimal values first."""
    for parsed_data in parsed_data_list:
        hex_line = ",".join(str(value) for value in parsed_data[0])
        print(hex_line)

def print_all_decimal(parsed_data_list):
    """Print all the decimal values in CSV format."""
    for parsed_data in parsed_data_list:
        if parsed_data:
            decimal_line = ",".join(f"{value:.2f}" if isinstance(value, float) else str(value) for value in parsed_data[1])
            print(decimal_line)
    
    # Extract and write decimal data to CSV
    decimal_data = [parsed_data[1] for parsed_data in parsed_data_list if parsed_data]
    write_decimal_to_csv('28jan2025_data.csv', decimal_data)

def read_and_print_data_packet(filename):
    """Read a data packet from the file and print all hex values first, then decimal values."""
    parsed_data_list = []
    with open(filename, 'r') as file:
        for line in file:
            parsed_data = parse_data_line(line)
            if parsed_data:
                parsed_data_list.append(parsed_data)
    
    # Print all hexadecimal values first
    print_all_hex(parsed_data_list)
    
    # Print all decimal values and log them to CSV
    print_all_decimal(parsed_data_list)

# Additional function to print filled data packet and total bytes
def read_and_print_filled_data_packet(filename):
    """Read a data packet and print filled hexadecimal values and total bytes."""
    with open(filename, 'r') as file:
        for line in file:
            # Split the data packet into hexadecimal values
            hex_values = line.split()
            
            # Fill each hexadecimal value with leading zeros if necessary
            filled_hex_values = [val.zfill(2) for val in hex_values]
            
            # Join the filled hexadecimal values into a single string
            filled_data_packet = ' '.join(filled_hex_values)
            
            # Count the number of hexadecimal values
            total_bytes = len(hex_values)
            
            print("Double byte:", filled_data_packet, ",Total bytes:", total_bytes)

# Call the function to print filled data packet and total bytes
# read_and_print_filled_data_packet('datalog1.txt')

# Call the function to print hex values and log decimal values to CSV
read_and_print_data_packet('datalog28jan25_original.txt')
