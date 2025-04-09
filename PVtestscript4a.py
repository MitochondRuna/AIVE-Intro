# trace generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

xlist = ["_01","_02","_03","_04","_05","_06"]
for x in xlist:


# create a new 'TIFF Series Reader'
    Workingimage = TIFFSeriesReader(registrationName='m11'+x, FileNames=['K:\\2023\Jul23 update ALL\MP3 u\Model_11 tiffs\My AIVE merge 13 test - paraview\MP3_m11'+x+'.tif'])
    Workingimage.UseCustomDataSpacing = 1
    Workingimage.CustomDataSpacing = [0.030013, 0.030013, 0.1]

# get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
    WorkingimageDisplay = Show(Workingimage, renderView1, 'UniformGridRepresentation')

# trace defaults for the display properties.
    WorkingimageDisplay.Representation = 'Outline'
    WorkingimageDisplay.ColorArrayName = ['POINTS', '']
    WorkingimageDisplay.SelectTCoordArray = 'None'
    WorkingimageDisplay.SelectNormalArray = 'None'
    WorkingimageDisplay.SelectTangentArray = 'None'
    WorkingimageDisplay.OSPRayScaleArray = 'Tiff Scalars'
    WorkingimageDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    WorkingimageDisplay.SelectOrientationVectors = 'None'
    WorkingimageDisplay.ScaleFactor = 1.08
    WorkingimageDisplay.SelectScaleArray = 'Tiff Scalars'
    WorkingimageDisplay.GlyphType = 'Arrow'
    WorkingimageDisplay.GlyphTableIndexArray = 'Tiff Scalars'
    WorkingimageDisplay.GaussianRadius = 0.054000000000000006
    WorkingimageDisplay.SetScaleArray = ['POINTS', 'Tiff Scalars']
    WorkingimageDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    WorkingimageDisplay.OpacityArray = ['POINTS', 'Tiff Scalars']
    WorkingimageDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    WorkingimageDisplay.DataAxesGrid = 'GridAxesRepresentation'
    WorkingimageDisplay.PolarAxes = 'PolarAxesRepresentation'
    WorkingimageDisplay.ScalarOpacityUnitDistance = 0.07774812167408818
    WorkingimageDisplay.OpacityArrayName = ['POINTS', 'Tiff Scalars']
    WorkingimageDisplay.IsosurfaceValues = [124.0]

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
    WorkingimageDisplay.OSPRayScaleFunction.Points = [-1.267206730269358, 0.0, 0.5, 0.0, 24.196090213803426, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    WorkingimageDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 248.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    WorkingimageDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 248.0, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
    WorkingimageDisplay.SliceFunction.Origin = [4.9971645, 4.9971645, 5.4]

# reset view to fit data
    renderView1.ResetCamera()

# get the material library
    materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
    renderView1.Update()

# set scalar coloring
    ColorBy(WorkingimageDisplay, ('POINTS', 'Tiff Scalars'))

# rescale color and/or opacity maps used to include current data range
    WorkingimageDisplay.RescaleTransferFunctionToDataRange(True, True)

# change representation type
    WorkingimageDisplay.SetRepresentationType('Volume')

# get color transfer function/color map for 'TiffScalars'
    tiffScalarsLUT = GetColorTransferFunction('TiffScalars')

# get opacity transfer function/opacity map for 'TiffScalars'
    tiffScalarsPWF = GetOpacityTransferFunction('TiffScalars')

# create a new 'Contour'
    contour1 = Contour(registrationName=('Contour'+x), Input=Workingimage)
    contour1.ContourBy = ['POINTS', 'Tiff Scalars']
    contour1.ComputeGradients = 1
    contour1.Isosurfaces = [124.0]
    contour1.PointMergeMethod = 'Uniform Binning'

# Properties modified on contour1
    contour1.Isosurfaces = [48.0]
    contour1.PointMergeMethod = 'Octree Binning'

# show data in view
    contour1Display = Show(contour1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
    contour1Display.Representation = 'Surface'
    contour1Display.ColorArrayName = ['POINTS', 'Tiff Scalars']
    contour1Display.LookupTable = tiffScalarsLUT
    contour1Display.SelectTCoordArray = 'None'
    contour1Display.SelectNormalArray = 'Normals'
    contour1Display.SelectTangentArray = 'None'
    contour1Display.OSPRayScaleArray = 'Tiff Scalars'
    contour1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    contour1Display.SelectOrientationVectors = 'Gradients'
    contour1Display.ScaleFactor = 0.8960087716579438
    contour1Display.SelectScaleArray = 'Tiff Scalars'
    contour1Display.GlyphType = 'Arrow'
    contour1Display.GlyphTableIndexArray = 'Tiff Scalars'
    contour1Display.GaussianRadius = 0.04480043858289719
    contour1Display.SetScaleArray = ['POINTS', 'Tiff Scalars']
    contour1Display.ScaleTransferFunction = 'PiecewiseFunction'
    contour1Display.OpacityArray = ['POINTS', 'Tiff Scalars']
    contour1Display.OpacityTransferFunction = 'PiecewiseFunction'
    contour1Display.DataAxesGrid = 'GridAxesRepresentation'
    contour1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
    contour1Display.OSPRayScaleFunction.Points = [-1.267206730269358, 0.0, 0.5, 0.0, 24.196090213803426, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    contour1Display.ScaleTransferFunction.Points = [64.0, 0.0, 0.5, 0.0, 64.015625, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    contour1Display.OpacityTransferFunction.Points = [64.0, 0.0, 0.5, 0.0, 64.015625, 1.0, 0.5, 0.0]

# show color bar/color legend
    contour1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
    renderView1.Update()


#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

# get layout
layout1 = GetLayout()

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1142, 552)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [4.997164726257324, 4.997164726257324, 39.76379371947567]
renderView1.CameraFocalPoint = [4.997164726257324, 4.997164726257324, 5.400000095367432]
renderView1.CameraParallelScale = 8.894004251891785

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
