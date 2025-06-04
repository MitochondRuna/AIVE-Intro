import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

# Function to save configuration using save-as dialog
def save_config():
    spacing = [
        float(custom_data_spacing_entry_x.get()),
        float(custom_data_spacing_entry_y.get()),
        float(custom_data_spacing_entry_z.get())
    ]
    isosurface_value = float(contour_isosurface_value_entry.get())
    folder_path = folder_path_entry.get()
    file_names = select_files_entry.get().split(';')

    config = {
        "folder": folder_path,
        "file_names": file_names,
        "spacing": spacing,
        "isosurface_value": isosurface_value
    }

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="Save Config As"
    )
    if not file_path:
        return

    with open(file_path, 'w') as f:
        json.dump(config, f, indent=4)

    messagebox.showinfo("Success", f"Configuration saved to:\n{file_path}")

# Select folder for data files
def choose_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path + "/")

# Load existing config JSON
def load_existing_config_file():
    file_path = filedialog.askopenfilename(
        title="Select a config file",
        filetypes=[("JSON files", "*.json")]
    )
    if not file_path:
        return

    with open(file_path, 'r') as f:
        config = json.load(f)

    folder_path = config.get('folder', '')
    file_names = config.get('file_names', [])
    spacing = config.get('spacing', [0.03, 0.03, 0.1])
    isosurface_value = config.get('isosurface_value', 48.0)

    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

    custom_data_spacing_entry_x.delete(0, tk.END)
    custom_data_spacing_entry_x.insert(0, str(spacing[0]))
    custom_data_spacing_entry_y.delete(0, tk.END)
    custom_data_spacing_entry_y.insert(0, str(spacing[1]))
    custom_data_spacing_entry_z.delete(0, tk.END)
    custom_data_spacing_entry_z.insert(0, str(spacing[2]))

    contour_isosurface_value_entry.delete(0, tk.END)
    contour_isosurface_value_entry.insert(0, str(isosurface_value))

    select_files_entry.delete(0, tk.END)
    select_files_entry.insert(0, ';'.join(file_names))

    messagebox.showinfo("Success", "Configuration loaded successfully!")

def exit_program():
    root.destroy()

# Select multiple data files
def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Files",
        filetypes=[("TIFF files", "*.tif"), ("All files", "*.*")]
    )

    file_names = [os.path.basename(path) for path in file_paths]
    select_files_entry.delete(0, tk.END)
    select_files_entry.insert(0, ';'.join(file_names))

# Create the main application window
root = tk.Tk()
root.title("JSON Config File Generator")
root.geometry("620x400")  # Slightly widened to avoid overlap

row_spacing = 40

# Folder Path (for data files)
tk.Label(root, text="Folder Path (for data files):").place(x=30, y=20)
folder_path_entry = tk.Entry(root, width=43)
folder_path_entry.place(x=240, y=20)
choose_folder_button = tk.Button(root, text="...", width=3, command=choose_folder)
choose_folder_button.place(x=540, y=18)

# Custom Data Spacing
tk.Label(root, text="Custom Data Spacing (x, y, z):").place(x=30, y=20 + row_spacing * 1)
custom_data_spacing_entry_x = tk.Entry(root, width=10)
custom_data_spacing_entry_x.insert(0, "0.030013")
custom_data_spacing_entry_x.place(x=240, y=20 + row_spacing * 1)
custom_data_spacing_entry_y = tk.Entry(root, width=10)
custom_data_spacing_entry_y.insert(0, "0.030013")
custom_data_spacing_entry_y.place(x=320, y=20 + row_spacing * 1)
custom_data_spacing_entry_z = tk.Entry(root, width=10)
custom_data_spacing_entry_z.insert(0, "0.1")
custom_data_spacing_entry_z.place(x=400, y=20 + row_spacing * 1)

# Contour Isosurface Value
tk.Label(root, text="Contour Isosurface Value:").place(x=30, y=20 + row_spacing * 2)
contour_isosurface_value_entry = tk.Entry(root, width=10)
contour_isosurface_value_entry.insert(0, "48.0")
contour_isosurface_value_entry.place(x=240, y=20 + row_spacing * 2)

# Selected Files
tk.Label(root, text="Selected Files:").place(x=30, y=20 + row_spacing * 3)
select_files_entry = tk.Entry(root, width=43)
select_files_entry.place(x=240, y=20 + row_spacing * 3)
select_file_button = tk.Button(root, text="...", width=3, command=select_files)
select_file_button.place(x=540, y=20 + row_spacing * 3 - 2)

# Action Buttons
load_config_button = tk.Button(root, text="Load Config", width=15, command=load_existing_config_file)
load_config_button.place(x=50, y=20 + row_spacing * 5)

save_button = tk.Button(root, text="Save Config", width=15, command=save_config)
save_button.place(x=220, y=20 + row_spacing * 5)

exit_program_button = tk.Button(root, text="Exit", width=10, command=exit_program)
exit_program_button.place(x=400, y=20 + row_spacing * 5)

# Start the GUI
root.mainloop()
