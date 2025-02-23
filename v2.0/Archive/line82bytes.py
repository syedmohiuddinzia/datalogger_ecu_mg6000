# Define input and output file paths (use raw string `r` to handle backslashes)
input_file = r"DataLogger_V2.0/data-20feb25/2.txt"
output_file = r"DataLogger_V2.0/data-20feb25/output_2.txt"

# Read the input file
with open(input_file, "r") as file:
    data = file.read().split()  # Split the data by spaces

# Define the chunk size
chunk_size = 82

# Split data into lines of 82 bytes
chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# Write the formatted output
with open(output_file, "w") as file:
    for chunk in chunks:
        file.write(" ".join(chunk) + "\n")

print("File processing complete. The output is saved in 'output.txt'.")
