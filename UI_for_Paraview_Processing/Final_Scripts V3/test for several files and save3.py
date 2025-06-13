from paraview.simple import *
import os
import json

# Disable automatic camera reset when showing data
paraview.simple._DisableFirstRenderCameraReset()

# Load configuration from JSON file
config_path = r'E:\AIVE_main\paraview work\Test for one file in Paraview\Project Part 1\config_changable.json'
with open(config_path, 'r') as f:
    config = json.load(f)

# Read parameters from config
export_x3d = config.get("export_x3d", False)
export_stl = config.get("export_stl", False)
folder = config.get("folder", "")
file_names = config.get("file_names", [])
spacing = config.get("spacing", [1.0, 1.0, 1.0])
isosurface_value = config.get("isosurface_value", 0.5)

# Create or get the active render view
renderView1 = GetActiveViewOrCreate('RenderView')
contour_sources = []

# Process each input file and create corresponding Contour
for file_name in file_names:
    full_path = os.path.join(folder, file_name)

    # Create TIFF reader
    reader = TIFFSeriesReader(registrationName=file_name, FileNames=[full_path])
    reader.UseCustomDataSpacing = 1
    reader.CustomDataSpacing = spacing
    UpdatePipeline(time=0.0, proxy=reader)

    base_name = os.path.splitext(file_name)[0]

    # Create Contour
    contour = Contour(registrationName=f'Contour_{base_name}', Input=reader)
    contour.ComputeGradients = 1
    contour.Isosurfaces = [isosurface_value]
    UpdatePipeline(time=0.0, proxy=contour)

    # Show in render view
    contourDisplay = Show(contour, renderView1, 'GeometryRepresentation')
    contourDisplay.Representation = 'Surface'
    contourDisplay.SetScalarBarVisibility(renderView1, True)

    contour_sources.append((f'Contour_{base_name}', contour))  # Save name and source

# Reset the camera to fit all
renderView1.ResetCamera()

# Export .x3d if enabled
if export_x3d:
    print("\nExporting .x3d file:")
    save_folder = input("Enter the folder path to save the .x3d file: ").strip()
    if not save_folder.endswith(os.sep):
        save_folder += os.sep

    if not os.path.exists(save_folder):
        print(f"Folder does not exist: {save_folder}")
        print("Export aborted.")
    else:
        save_filename = input("Enter the filename for the .x3d file (e.g. myExport.x3d): ").strip()
        if not save_filename.lower().endswith('.x3d'):
            print("Warning: filename does not end with '.x3d', appending extension.")
            save_filename += '.x3d'

        save_path = os.path.join(save_folder, save_filename)
        ExportView(save_path, view=renderView1)
        print(f".x3d file successfully saved to: {save_path}")

# Export .stl if enabled
if export_stl:
    print("\nExporting all Contour sources as .stl files...")

    save_folder = input("Enter folder path to save STL files: ").strip()
    if not save_folder.endswith(os.sep):
        save_folder += os.sep

    if not os.path.exists(save_folder):
        print(f"Folder does not exist: {save_folder}")
        print("STL export aborted.")
    else:
        for name, source in contour_sources:
            save_path = os.path.join(save_folder, f"{name}.stl")
            SaveData(save_path, proxy=source)
            print(f"Saved: {save_path}")
