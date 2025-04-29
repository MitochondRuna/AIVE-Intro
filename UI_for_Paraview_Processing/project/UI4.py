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

def Run_Process():    # Get values from the GUI
    # Get values from the GUI
    folder_path = folder_path_entry.get()
    file_prefix = file_prefix_entry.get()
    registration_prefix = registration_prefix_entry.get()
    custom_data_spacing = [
        float(custom_data_spacing_entry_x.get()),
        float(custom_data_spacing_entry_y.get()),
        float(custom_data_spacing_entry_z.get())
    ]
    contour_isosurface_value = float(contour_isosurface_value_entry.get())

    # Ensure folder path ends with a slash
    if not folder_path.endswith('/'):
        folder_path += '/'

    # Check if the folder exists
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "Folder does not exist.")
        return

    # Get list of relevant .tif files
    file_list = sorted([
        f for f in os.listdir(folder_path)
        if f.startswith(file_prefix) and f.endswith(".tif")
    ])
    xlist = [os.path.splitext(f)[0].replace(file_prefix, "") for f in file_list]

    print("Detected files:", xlist)

    # Loop through files
    for x in xlist:
        file_path = folder_path + file_prefix + x + ".tif"

        # Load image
        Workingimage = TIFFSeriesReader(
            registrationName=registration_prefix + x,
            FileNames=[file_path]
        )
        Workingimage.UseCustomDataSpacing = 1
        Workingimage.CustomDataSpacing = custom_data_spacing

        # Get render view
        renderView1 = GetActiveViewOrCreate('RenderView')
        WorkingimageDisplay = Show(Workingimage, renderView1, 'UniformGridRepresentation')
        WorkingimageDisplay.Representation = 'Outline'
        WorkingimageDisplay.ColorArrayName = ['POINTS', '']
        WorkingimageDisplay.OSPRayScaleArray = 'Tiff Scalars'
        WorkingimageDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
        WorkingimageDisplay.SelectOrientationVectors = 'None'
        WorkingimageDisplay.ScaleFactor = 1.08
        WorkingimageDisplay.SelectScaleArray = 'Tiff Scalars'
        WorkingimageDisplay.GlyphType = 'Arrow'
        WorkingimageDisplay.GlyphTableIndexArray = 'Tiff Scalars'
        WorkingimageDisplay.GaussianRadius = 0.054
        WorkingimageDisplay.SetScaleArray = ['POINTS', 'Tiff Scalars']
        WorkingimageDisplay.ScaleTransferFunction = 'PiecewiseFunction'
        WorkingimageDisplay.OpacityArray = ['POINTS', 'Tiff Scalars']
        WorkingimageDisplay.OpacityTransferFunction = 'PiecewiseFunction'
        WorkingimageDisplay.DataAxesGrid = 'GridAxesRepresentation'
        WorkingimageDisplay.PolarAxes = 'PolarAxesRepresentation'
        WorkingimageDisplay.ScalarOpacityUnitDistance = 0.07774812167408818
        WorkingimageDisplay.OpacityArrayName = ['POINTS', 'Tiff Scalars']
        WorkingimageDisplay.IsosurfaceValues = [124.0]

        # Transfer function setup
        WorkingimageDisplay.OSPRayScaleFunction.Points = [-1.267, 0.0, 0.5, 0.0, 24.196, 1.0, 0.5, 0.0]
        WorkingimageDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 248.0, 1.0, 0.5, 0.0]
        WorkingimageDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 248.0, 1.0, 0.5, 0.0]
        WorkingimageDisplay.SliceFunction.Origin = [4.9971645, 4.9971645, 5.4]

        renderView1.ResetCamera()
        materialLibrary1 = GetMaterialLibrary()
        renderView1.Update()

        ColorBy(WorkingimageDisplay, ('POINTS', 'Tiff Scalars'))
        WorkingimageDisplay.RescaleTransferFunctionToDataRange(True, True)
        WorkingimageDisplay.SetRepresentationType('Volume')

        # Transfer functions
        tiffScalarsLUT = GetColorTransferFunction('TiffScalars')
        tiffScalarsPWF = GetOpacityTransferFunction('TiffScalars')

        # Create and show contour
        contour1 = Contour(registrationName='Contour' + x, Input=Workingimage)
        contour1.ContourBy = ['POINTS', 'Tiff Scalars']
        contour1.ComputeGradients = 1
        contour1.Isosurfaces = [contour_isosurface_value]
        contour1.PointMergeMethod = 'Octree Binning'

        contour1Display = Show(contour1, renderView1, 'GeometryRepresentation')
        contour1Display.Representation = 'Surface'
        contour1Display.ColorArrayName = ['POINTS', 'Tiff Scalars']
        contour1Display.LookupTable = tiffScalarsLUT
        contour1Display.SelectNormalArray = 'Normals'
        contour1Display.OSPRayScaleArray = 'Tiff Scalars'
        contour1Display.OSPRayScaleFunction = 'PiecewiseFunction'
        contour1Display.SelectOrientationVectors = 'Gradients'
        contour1Display.ScaleFactor = 0.896
        contour1Display.SelectScaleArray = 'Tiff Scalars'
        contour1Display.GlyphType = 'Arrow'
        contour1Display.GlyphTableIndexArray = 'Tiff Scalars'
        contour1Display.GaussianRadius = 0.0448
        contour1Display.SetScaleArray = ['POINTS', 'Tiff Scalars']
        contour1Display.ScaleTransferFunction = 'PiecewiseFunction'
        contour1Display.OpacityArray = ['POINTS', 'Tiff Scalars']
        contour1Display.OpacityTransferFunction = 'PiecewiseFunction'
        contour1Display.DataAxesGrid = 'GridAxesRepresentation'
        contour1Display.PolarAxes = 'PolarAxesRepresentation'

        # Contour transfer function
        contour1Display.OSPRayScaleFunction.Points = [-1.267, 0.0, 0.5, 0.0, 24.196, 1.0, 0.5, 0.0]
        contour1Display.ScaleTransferFunction.Points = [64.0, 0.0, 0.5, 0.0, 64.015625, 1.0, 0.5, 0.0]
        contour1Display.OpacityTransferFunction.Points = [64.0, 0.0, 0.5, 0.0, 64.015625, 1.0, 0.5, 0.0]

        contour1Display.SetScalarBarVisibility(renderView1, True)
        renderView1.Update()

    # Optional final rendering or screenshot
    # RenderAllViews()
    # SaveScreenshot("output.png")
    messagebox.showinfo("Success", "Process completed successfully.")

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

Run_Process_button = tk.Button(root, text="Run Process", command=Run_Process)
Run_Process_button.pack()

# Start the GUI event loop
root.mainloop()
