import os
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read(r'E:\AIVE_main\paraview work\Test for one file in Paraview\project\config_changable.ini')

# Extract values from the configuration file
folder_path = config.get('GENERAL', 'folder_path')
file_prefix = config.get('GENERAL', 'file_prefix')
registration_prefix = config.get('GENERAL', 'registration_prefix')
custom_data_spacing = list(map(float, config.get('GENERAL', 'custom_data_spacing').split(',')))
contour_isosurface_value = float(config.get('GENERAL', 'contour_isosurface_value'))

# --- Automatically generate xlist from file names ---
file_list = sorted([f for f in os.listdir(folder_path) if f.startswith(file_prefix) and f.endswith(".tif")])
xlist = [os.path.splitext(f)[0].replace(file_prefix, "") for f in file_list]

# --- Check xlist ---
print("Detected files:", xlist)

# --- Import necessary Paraview module ---
from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

# --- Loop through all images defined in xlist ---
for x in xlist:
    # Construct full file path
    file_path = folder_path + file_prefix + x + ".tif"

    # Create TIFF reader for each image
    Workingimage = TIFFSeriesReader(
        registrationName=registration_prefix + x,
        FileNames=[file_path]
    )
    Workingimage.UseCustomDataSpacing = 1
    Workingimage.CustomDataSpacing = custom_data_spacing

    # Get active render view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # Show the TIFF image in the render view
    WorkingimageDisplay = Show(Workingimage, renderView1, 'UniformGridRepresentation')

    # Set default display properties
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
    WorkingimageDisplay.IsosurfaceValues = [124.0]  # Not relevant when using volume

    # Initialize transfer functions
    WorkingimageDisplay.OSPRayScaleFunction.Points = [-1.267, 0.0, 0.5, 0.0, 24.196, 1.0, 0.5, 0.0]
    WorkingimageDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 248.0, 1.0, 0.5, 0.0]
    WorkingimageDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 248.0, 1.0, 0.5, 0.0]

    # Set slicing origin
    WorkingimageDisplay.SliceFunction.Origin = [4.9971645, 4.9971645, 5.4]

    # Reset camera to fit the current image
    renderView1.ResetCamera()

    # Load material library (used for rendering)
    materialLibrary1 = GetMaterialLibrary()

    # Update view
    renderView1.Update()

    # Enable scalar coloring
    ColorBy(WorkingimageDisplay, ('POINTS', 'Tiff Scalars'))

    # Adjust color and opacity maps to match data range
    WorkingimageDisplay.RescaleTransferFunctionToDataRange(True, True)

    # Switch display to volume rendering
    WorkingimageDisplay.SetRepresentationType('Volume')

    # Get color and opacity transfer functions
    tiffScalarsLUT = GetColorTransferFunction('TiffScalars')
    tiffScalarsPWF = GetOpacityTransferFunction('TiffScalars')

    # Create contour based on the TIFF image
    contour1 = Contour(registrationName='Contour' + x, Input=Workingimage)
    contour1.ContourBy = ['POINTS', 'Tiff Scalars']
    contour1.ComputeGradients = 1
    contour1.Isosurfaces = [contour_isosurface_value]  # Use value defined at top
    contour1.PointMergeMethod = 'Octree Binning'

    # Show contour in the view
    contour1Display = Show(contour1, renderView1, 'GeometryRepresentation')

    # Set default display properties for the contour
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

    # Initialize transfer functions for the contour
    contour1Display.OSPRayScaleFunction.Points = [-1.267, 0.0, 0.5, 0.0, 24.196, 1.0, 0.5, 0.0]
    contour1Display.ScaleTransferFunction.Points = [64.0, 0.0, 0.5, 0.0, 64.015625, 1.0, 0.5, 0.0]
    contour1Display.OpacityTransferFunction.Points = [64.0, 0.0, 0.5, 0.0, 64.015625, 1.0, 0.5, 0.0]

    # Show the scalar bar (color legend)
    contour1Display.SetScalarBarVisibility(renderView1, True)

    # Update the view to apply changes
    renderView1.Update()

# Optional: Render all views if needed
# RenderAllViews()

# Optional: Save screenshot using SaveScreenshot("filename.png")
