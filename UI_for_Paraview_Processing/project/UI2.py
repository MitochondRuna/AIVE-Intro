import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import configparser

# Function to save configuration to config.ini
def save_config():
    config = configparser.ConfigParser()
    config['GENERAL'] = {
        'folder_path': folder_path_entry.get(),
        'file_prefix': file_prefix_entry.get(),
        'registration_prefix': registration_prefix_entry.get(),
        'custom_data_spacing': custom_data_spacing_entry_x.get() + ',' +
                               custom_data_spacing_entry_y.get() + ',' +
                               custom_data_spacing_entry_z.get(),
        'contour_isosurface_value': contour_isosurface_value_entry.get()
    }

    with open('config_changable.ini', 'w') as configfile:
        config.write(configfile)

    messagebox.showinfo("Success", "Configuration saved as config.ini")

def choose_folder():
    folder_path = filedialog.askdirectory() 
    if folder_path:  
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path + "/")  # Append a trailing slash

def Load_existing_config_file():

    config = configparser.ConfigParser()
    config.read(r'E:\AIVE_main\paraview work\Test for one file in Paraview\project\config_for_multiple_files.ini')

    # Extract values from the configuration file
    folder_path= config.get('GENERAL', 'folder_path')
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

    file_prefix = config.get('GENERAL', 'file_prefix')
    file_prefix_entry.delete(0, tk.END)
    file_prefix_entry.insert(0, file_prefix)

    registration_prefix = config.get('GENERAL', 'registration_prefix')
    registration_prefix_entry.delete(0, tk.END)
    registration_prefix_entry.insert(0, registration_prefix)

    custom_data_spacing = list(map(float, config.get('GENERAL', 'custom_data_spacing').split(',')))
    custom_data_spacing_entry_x.delete(0, tk.END)
    custom_data_spacing_entry_x.insert(0, str(custom_data_spacing[0]))
    custom_data_spacing_entry_y.delete(0, tk.END)
    custom_data_spacing_entry_y.insert(0, str(custom_data_spacing[1]))
    custom_data_spacing_entry_z.delete(0, tk.END)
    custom_data_spacing_entry_z.insert(0, str(custom_data_spacing[2]))

    contour_isosurface_value = float(config.get('GENERAL', 'contour_isosurface_value'))
    contour_isosurface_value_entry.delete(0, tk.END)
    contour_isosurface_value_entry.insert(0, str(contour_isosurface_value))

# Create the main application window
root = tk.Tk()
root.title("Config File Generator")
root.geometry("600x300")  # Slightly wider for better layout

# Row height spacing
row_spacing = 40

# Folder Path
tk.Label(root, text="Folder Path:").place(x=30, y=20)
folder_path_entry = tk.Entry(root, width=50)
# folder_path_entry.insert(0, "E:/AIVE_main/paraview work/Test for one file in Paraview/A2_Output/")  # Default value
folder_path_entry.place(x=180, y=20)

# File Prefix
tk.Label(root, text="File Prefix:").place(x=30, y=20 + row_spacing)
file_prefix_entry=tk.Entry(root, width=50)
file_prefix_entry.insert(0, "MP3_Model5A")  # Default value
file_prefix_entry.place(x=180, y=20 + row_spacing)

# Registration Prefix
tk.Label(root, text="Registration Prefix:").place(x=30, y=20 + row_spacing * 2)
registration_prefix_entry=tk.Entry(root, width=50)
registration_prefix_entry.insert(0, "Model5A")
registration_prefix_entry.place(x=180, y=20 + row_spacing * 2)

# Custom Data Spacing (x, y, z)
tk.Label(root, text="Custom Data Spacing (x,y,z):").place(x=30, y=20 + row_spacing * 3)
custom_data_spacing_entry_x = tk.Entry(root, width=10)
custom_data_spacing_entry_x.insert(0, "0.030013")
custom_data_spacing_entry_x.place(x=240, y=20 + row_spacing * 3)

custom_data_spacing_entry_y = tk.Entry(root, width=10)
custom_data_spacing_entry_y.insert(0, "0.030013")
custom_data_spacing_entry_y.place(x=320, y=20 + row_spacing * 3)

custom_data_spacing_entry_z = tk.Entry(root, width=10)
custom_data_spacing_entry_z.insert(0, "0.1")
custom_data_spacing_entry_z.place(x=400, y=20 + row_spacing * 3)

# Contour Isosurface Value
tk.Label(root, text="Contour Isosurface Value:").place(x=30, y=20 + row_spacing * 4)
contour_isosurface_value_entry = tk.Entry(root, width=50)
contour_isosurface_value_entry.insert(0, "48.0")
contour_isosurface_value_entry.place(x=240, y=20 + row_spacing * 4)

# Save Button
save_button = tk.Button(root, text="Save Configuration", command=save_config)
save_button.place(x=240, y=20 + row_spacing * 5)

choose_folder_button = tk.Button(root, text="Select Folder", command=choose_folder)
choose_folder_button.place(x=30, y=20 + row_spacing * 5)

load_config_button = tk.Button(root, text="Load existing config file", command=Load_existing_config_file)
load_config_button.place(x=420, y=20 + row_spacing * 5)

# Start the GUI event loop
root.mainloop()
