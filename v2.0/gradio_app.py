import pandas as pd
import plotly.graph_objects as go
import gradio as gr

# Define column names explicitly
column_names = [
    "Seconds", "Injection Pulse Width 1 (us)", "Injection Pulse Width 2 (us)", "RPM", "Ignition Advance Angle (deg)",
    "Injection Event Scheduling", "Engine Status Ready", "Engine Status Crank", "Engine Status StartW",
    "Engine Status Warmup", "Engine Status TPSAEN", "Engine Status TPSDEN", "Air-Fuel Ratio Target 1", "Air-Fuel Ratio Target 2",
    "WBO2 Enabled 1", "WBO2 Enabled 2", "Barometric Pressure (kPa)", "Manifold Absolute Pressure (kPa)",
    "Manifold Air Temperature (deg C)", "Cylinder Temperature (deg C)", "Throttle Position (%)", "Battery Voltage (V)"
]

# Function to read CSV file and process data
def process_csv(file):
    # Read the uploaded CSV file
    df = pd.read_csv(file.name, names=column_names, header=0)
    return df

# Function to generate an interactive Plotly graph
def plot_data(df, selected_parameters):
    fig = go.Figure()
    
    for param in selected_parameters:
        if param in df.columns:
            fig.add_trace(go.Scatter(
                # Convert 'Seconds' to 'Time' in HH:MM:SS format
                x = pd.to_timedelta(df['Seconds'], unit='s').astype(str).str.slice(start=7),  # Keep HH:MM:SS format
                # x=df['Seconds'],  # Assuming 'Seconds' is the time axis
                y=df[param], 
                mode='lines', 
                name=param
            ))
    
    # Update layout for fullscreen & better visibility
    fig.update_layout(
        title="Selected Parameters Over Time",
        xaxis_title="Time (Seconds)",
        yaxis_title="Values",
        xaxis=dict(tickangle=-90, showgrid=True),
        yaxis=dict(showgrid=True),
        legend=dict(x=0, y=1),
        width=1400,  # Increase width
        height=1000,  # Increase height
        margin=dict(l=20, r=20, t=50, b=100)  # Adjust margins for better display
    )
    
    return fig

# Gradio UI
param_list = column_names[1:]  # Exclude 'Seconds' for plotting

with gr.Blocks(css="body { overflow-x: auto; }") as demo:
    gr.Markdown("# ECU Data Visualization")
    gr.Markdown("### Upload a CSV file and select parameters to plot against time using an interactive Plotly chart.")
    
    # Upload CSV file
    file_input = gr.File(label="Upload CSV File")
    
    # Checkbox group for selecting parameters to plot
    selected_params = gr.CheckboxGroup(param_list, label="Select parameters to plot")
    
    # Plot output
    plot_output = gr.Plot()
    
    # Button to clear the plot
    clear_button = gr.Button("Clear")
    
    # Actions for file upload and parameter selection
    def update_plot(file, selected_params):
        if file:
            df = process_csv(file)
            return plot_data(df, selected_params)
    
    file_input.change(fn=update_plot, inputs=[file_input, selected_params], outputs=plot_output)
    selected_params.change(fn=update_plot, inputs=[file_input, selected_params], outputs=plot_output)
    clear_button.click(fn=lambda: None, inputs=[], outputs=[plot_output])

# Launch with `share=True` for public access
demo.launch(share=True)
