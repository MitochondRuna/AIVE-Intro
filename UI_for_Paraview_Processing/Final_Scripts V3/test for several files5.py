from paraview.simple import *
import os
import json
#### Disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

with open(r'E:\AIVE_main\paraview work\Test for one file in Paraview\Project Part 1\config_changable.json', 'r') as f:
    config = json.load(f)

folder = config['folder']
file_names = config['file_names']
spacing = config['spacing']
isosurface_value = config['isosurface_value']

# Loop through all files
for file_name in file_names:
    full_path = os.path.join(folder, file_name)

    # Create TIFF reader
    reader = TIFFSeriesReader(registrationName=file_name, FileNames=[full_path])
    reader.UseCustomDataSpacing = 1
    reader.CustomDataSpacing = spacing

    # Update pipeline for reader
    UpdatePipeline(time=0.0, proxy=reader)

    # Remove '.tif' suffix from file name
    base_name = os.path.splitext(file_name)[0]

    # Create contour with cleaned name
    contour = Contour(registrationName=f'Contour_{base_name}', Input=reader)
    contour.ComputeGradients = 1
    contour.Isosurfaces = [isosurface_value]

    # Update pipeline for contour
    UpdatePipeline(time=0.0, proxy=contour)
