# state file generated using paraview version 5.13.3
import os
import json
import paraview
paraview.compatibility.major = 5
paraview.compatibility.minor = 13

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# read config file
def ReadConfigFile(configPath):
    # load config
    with open(configPath) as f:
        config = json.load(f)

    # retrieve paths and variables
    InputFolder = config['inputFolder']
    CustomDataSpacing = config['parameters']['customDataSpacing']
    Isosurfaces = config['parameters']['isosurfaces']

    return InputFolder, CustomDataSpacing, Isosurfaces

def LoadConfig(configPath):
    with open(configPath) as f:
        return json.load(f)

# open all .tif files in a selected folder
def ProcessFolder(inputFolder, CustomDataSpacing, Isosurfaces):
    counter = 0
    for fileName in os.listdir(inputFolder):
        if fileName.endswith(".tif"):
            inputFile = os.path.join(inputFolder, fileName)
            counter += 1

            # create a new 'TIFF Series Reader'
            model = TIFFSeriesReader(registrationName=fileName, FileNames=[inputFile])
            model.UseCustomDataSpacing = 1
            model.CustomDataSpacing = CustomDataSpacing

            # create a new 'Contour'
            contour = Contour(registrationName='Contour' + str(counter), Input=model)
            contour.ContourBy = ['POINTS', 'Tiff Scalars']
            contour.ComputeGradients = 1
            contour.Isosurfaces = Isosurfaces
            contour.PointMergeMethod = 'Uniform Binning'

# ----------------------------------------------------------------
# main script execution
# ----------------------------------------------------------------

# currently use an absolute path for the config file
configPath = "/Users/cheryl/Documents/AIVE/Paraview/AIVE merge - Paraview/config.json"
InputFolder, CustomDataSpacing, Isosurfaces = ReadConfigFile(configPath)
ProcessFolder(InputFolder, CustomDataSpacing, Isosurfaces)