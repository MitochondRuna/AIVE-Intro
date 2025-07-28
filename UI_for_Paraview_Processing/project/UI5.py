import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import configparser
import os

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
        'contour_isosurface_value': contour_isosurface_value_entry.get(),
        'selected_files': select_files_entry.get(),
    }

    with open('config_changable.ini', 'w') as configfile:
        config.write(configfile)

    messagebox.showinfo("Success", "Configuration saved as config_changable.ini")

def choose_folder():
    folder_path = filedialog.askdirectory() 
    if folder_path:  
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path + "/")  # Append a trailing slash

def Identify_prefix():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("TIFF files", "*.tif")]
    )
    if not file_path:
        return
    
    # Extract the prefix from the selected file name
    file_name = file_path.split("/")[-1]  # Get the file name from the full path
    registration_prefix = file_name.split("_")[1]  # Assuming the prefix is before the first underscore
    file_prefix = file_name.split("_")[0] +'_'+file_name.split("_")[1] # Assuming the prefix is before the first underscore

    # Set the prefix in the entry field
    file_prefix_entry.delete(0, tk.END)
    file_prefix_entry.insert(0, file_prefix)

    # Set the registration prefix in the entry field
    registration_prefix_entry.delete(0, tk.END)
    registration_prefix_entry.insert(0, registration_prefix)

def Load_existing_config_file():

    file_path = filedialog.askopenfilename(
        title="Select a config file",
        filetypes=[("INI files", "*.ini")]
    )
    if not file_path:
        return
    
    config = configparser.ConfigParser()
    config.read(file_path)

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

    messagebox.showinfo("Success", "Configuration loaded successfully!")

def exit_program():
    root.destroy()  # 或 root.quit()

def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Files",
        filetypes=[("TIFF files", "*.tif"), ("All files", "*.*")]
    )

    numbers = []

    for file_path in file_paths:
        file_name = os.path.basename(file_path)  # Get the file name from the full path, such as MP3_Model5A_01.tif
        basename = os.path.splitext(file_name)[0]   # Remove the file extension, such as MP3_Model5A_01
        
        # Split the basename by underscore and check if the last part is a number
        parts = basename.rsplit('_', 1)
        if len(parts) == 2 and parts[1].isdigit():
            numbers.append(parts[1])  # Extract the number part
        else:
            print(f"Warning: {file_name} does not match expected pattern.")

    print("Extracted numbers:", numbers)
    select_files_entry.delete(0, tk.END)
    select_files_entry.insert(0, numbers)


def my_add(a, b):
    return a + b


print(my_add(1,2))
print(my_add)

# Create the main application window
root = tk.Tk()
root.title("Config File Generator")
root.geometry("600x400")  # Slightly wider for better layout

# Row height spacing
row_spacing = 40

# Folder Path
tk.Label(root, text="Folder Path:").place(x=30, y=20)
folder_path_entry = tk.Entry(root, width=45)
folder_path_entry.place(x=180, y=20)
choose_folder_button = tk.Button(root, text="...", width=3, command=choose_folder)
choose_folder_button.place(x=500, y=20)

# File Prefix
tk.Label(root, text="File Prefix:").place(x=30, y=20 + row_spacing)
file_prefix_entry = tk.Entry(root, width=45)
file_prefix_entry.insert(0, "MP3_Model5A")
file_prefix_entry.place(x=180, y=20 + row_spacing)
Identify_prefix_button = tk.Button(root, text="...", width=3, command=Identify_prefix)
Identify_prefix_button.place(x=500, y=20 + row_spacing)

# Registration Prefix
tk.Label(root, text="Registration Prefix:").place(x=30, y=20 + row_spacing * 2)
registration_prefix_entry = tk.Entry(root, width=45)
registration_prefix_entry.insert(0, "Model5A")
registration_prefix_entry.place(x=180, y=20 + row_spacing * 2)

# Custom Data Spacing
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
contour_isosurface_value_entry = tk.Entry(root, width=10)
contour_isosurface_value_entry.insert(0, "48.0")
contour_isosurface_value_entry.place(x=240, y=20 + row_spacing * 4)

# Selected Files
tk.Label(root, text="Selected files:").place(x=30, y=20 + row_spacing * 5)
select_files_entry = tk.Entry(root, width=45)
select_files_entry.place(x=180, y=20 + row_spacing * 5)
select_file_button = tk.Button(root, text="...", width=3, command=select_files)
select_file_button.place(x=500, y=20 + row_spacing * 5)

# Action Buttons
load_config_button = tk.Button(root, text="Load Config", width=15, command=Load_existing_config_file)
load_config_button.place(x=50, y=20 + row_spacing * 7)

save_button = tk.Button(root, text="Save Config", width=15, command=save_config)
save_button.place(x=220, y=20 + row_spacing * 7)

exit_program_button = tk.Button(root, text="Exit", width=10, command=exit_program)
exit_program_button.place(x=400, y=20 + row_spacing * 7)

# Start the GUI event loop
root.mainloop()
