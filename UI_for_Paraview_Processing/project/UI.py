import tkinter as tk
from tkinter import messagebox
import configparser

# Function to save configuration to config.ini
def save_config():
    config = configparser.ConfigParser()
    config['GENERAL'] = {
        'folder_path': folder_path_entry.get(),
        'file_prefix': file_prefix_entry.get(),
        'registration_prefix': registration_prefix_entry.get(),
        'custom_data_spacing': custom_data_spacing_entry.get(),
        'contour_isosurface_value': contour_isosurface_value_entry.get()
    }

    with open('config_changable.ini', 'w') as configfile:
        config.write(configfile)

    messagebox.showinfo("Success", "Configuration saved as config.ini")

# Create the main application window
root = tk.Tk()
root.title("Config File Generator")  # Set the window title
root.geometry("500x300")  # Set window size

# Create labels and input fields for each parameter
tk.Label(root, text="Folder Path:").grid(row=0, column=0, sticky="e")
folder_path_entry = tk.Entry(root, width=50)
folder_path_entry.grid(row=0, column=1)

tk.Label(root, text="File Prefix:").grid(row=1, column=0, sticky="e")
file_prefix_entry = tk.Entry(root, width=50)
file_prefix_entry.grid(row=1, column=1)

tk.Label(root, text="Registration Prefix:").grid(row=2, column=0, sticky="e")
registration_prefix_entry = tk.Entry(root, width=50)
registration_prefix_entry.grid(row=2, column=1)

tk.Label(root, text="Custom Data Spacing (x,y,z):").grid(row=3, column=0, sticky="e")
custom_data_spacing_entry = tk.Entry(root, width=50)
custom_data_spacing_entry.insert(0, "0.030013,0.030013,0.1")  # Default value
custom_data_spacing_entry.grid(row=3, column=1)

tk.Label(root, text="Contour Isosurface Value:").grid(row=4, column=0, sticky="e")
contour_isosurface_value_entry = tk.Entry(root, width=50)
contour_isosurface_value_entry.insert(0, "48.0")  # Default value
contour_isosurface_value_entry.grid(row=4, column=1)

# Create a button to save the configuration
save_button = tk.Button(root, text="Save Configuration", command=save_config)
save_button.grid(row=5, column=1, pady=20)

# Start the GUI event loop
root.mainloop()