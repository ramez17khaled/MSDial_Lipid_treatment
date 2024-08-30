import os
import tkinter as tk
from tkinter import filedialog
import subprocess

def browse_button(entry):
    filename = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_param(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def run_tool():
    # Get input paths and parameters for NEG data
    input_path_NEG = entry_input_NEG.get()
    output_path_NEG = entry_output_NEG.get()
    param_path_NEG = entry_param_NEG.get()

    # Get input paths and parameters for POS data
    input_path_POS = entry_input_POS.get()
    output_path_POS = entry_output_POS.get()
    param_path_POS = entry_param_POS.get()

    # Create output directories for POS and NEG data if they don't exist
    os.makedirs(output_path_NEG, exist_ok=True)
    os.makedirs(output_path_POS, exist_ok=True)

    # Locate the MSDIAL executable using a relative path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    msdial_path = os.path.join(script_dir, "MSDIAL ver.4.9.221218 Windowsx64", "MsdialConsoleApp.exe")

    # Execute the tool command for NEG data
    tool_command_NEG = f'"{msdial_path}" lcmsdda -i {input_path_NEG} -o {output_path_NEG} -m {param_path_NEG}'
    print("Executing tool command (NEG):", tool_command_NEG)
    subprocess.run(tool_command_NEG, shell=True)

    # Execute the tool command for POS data
    tool_command_POS = f'"{msdial_path}" lcmsdda -i {input_path_POS} -o {output_path_POS} -m {param_path_POS}'
    print("Executing tool command (POS):", tool_command_POS)
    subprocess.run(tool_command_POS, shell=True)

root = tk.Tk()
root.title("MSDIAL Tool Command GUI")

# NEG data paths
label_input_NEG = tk.Label(root, text="Input Path (NEG):")
label_input_NEG.grid(row=0, column=0)
entry_input_NEG = tk.Entry(root, width=50)
entry_input_NEG.grid(row=0, column=1)
button_browse_input_NEG = tk.Button(root, text="Browse", command=lambda: browse_button(entry_input_NEG))
button_browse_input_NEG.grid(row=0, column=2)

label_output_NEG = tk.Label(root, text="Output Path (NEG):")
label_output_NEG.grid(row=1, column=0)
entry_output_NEG = tk.Entry(root, width=50)
entry_output_NEG.grid(row=1, column=1)
button_browse_output_NEG = tk.Button(root, text="Browse", command=lambda: browse_button(entry_output_NEG))
button_browse_output_NEG.grid(row=1, column=2)

label_param_NEG = tk.Label(root, text="Parameter File Path (NEG):")
label_param_NEG.grid(row=2, column=0)
entry_param_NEG = tk.Entry(root, width=50)
entry_param_NEG.grid(row=2, column=1)
button_browse_param_NEG = tk.Button(root, text="Browse", command=lambda: browse_param(entry_param_NEG))
button_browse_param_NEG.grid(row=2, column=2)

# POS data paths
label_input_POS = tk.Label(root, text="Input Path (POS):")
label_input_POS.grid(row=3, column=0)
entry_input_POS = tk.Entry(root, width=50)
entry_input_POS.grid(row=3, column=1)
button_browse_input_POS = tk.Button(root, text="Browse", command=lambda: browse_button(entry_input_POS))
button_browse_input_POS.grid(row=3, column=2)

label_output_POS = tk.Label(root, text="Output Path (POS):")
label_output_POS.grid(row=4, column=0)
entry_output_POS = tk.Entry(root, width=50)
entry_output_POS.grid(row=4, column=1)
button_browse_output_POS = tk.Button(root, text="Browse", command=lambda: browse_button(entry_output_POS))
button_browse_output_POS.grid(row=4, column=2)

label_param_POS = tk.Label(root, text="Parameter File Path (POS):")
label_param_POS.grid(row=5, column=0)
entry_param_POS = tk.Entry(root, width=50)
entry_param_POS.grid(row=5, column=1)
button_browse_param_POS = tk.Button(root, text="Browse", command=lambda: browse_param(entry_param_POS))
button_browse_param_POS.grid(row=5, column=2)

# Run button
button_run = tk.Button(root, text="Run Tool", command=run_tool)
button_run.grid(row=6, column=1)

root.mainloop()
