# --- User-Defined Parameters (Easy to Modify) ---
xlist = ["_01", "_02", "_03", "_04", "_05", "_06"]  # Suffixes for file names
base_path = "E:/AIVE_main/paraview work/Test for one file in Paraview/A2_Output/MP3_Model5A"  # Base path to TIFF files
registration_prefix = "Model5A"  # Prefix for registration name
custom_data_spacing = [0.030013, 0.030013, 0.1]  # Voxel spacing (x, y, z)
contour_isosurface_value = 48.0  # Isosurface value for contouring

# --- Import necessary Paraview module ---
from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()  # Prevent automatic camera reset

# --- Loop through all images defined in xlist ---
for x in xlist:
    # Create TIFF reader for each image
    Workingimage = TIFFSeriesReader(
        registrationName=registration_prefix + x,
        FileNames=[base_path + x + ".tif"]
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
