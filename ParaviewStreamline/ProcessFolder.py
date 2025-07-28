# ----------------------------------------------------------------
# ParaView Streamline Script (Input and Log)
# written by Cheryl Esther Lyandar
# ----------------------------------------------------------------

# state file generated using paraview version 5.13.3
import os
import json
import paraview
from datetime import datetime
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
    OutputFolder = config['outputFolder']
    CustomDataSpacing = config['parameters']['customDataSpacing']
    Isosurfaces = config['parameters']['isosurfaces']

    return InputFolder, OutputFolder, CustomDataSpacing, Isosurfaces

# load config file
def LoadConfig(configPath):
    with open(configPath) as f:
        return json.load(f)

# open all .tif files in a selected folder
def ProcessFolder(inputFolder, outputFolder, CustomDataSpacing, Isosurfaces):
    inputFiles = []

    for fileName in os.listdir(inputFolder):
        if fileName.endswith(".tif"):
            inputFile = os.path.join(inputFolder, fileName)
            inputFiles.append(inputFile)

            # create a new 'TIFF Series Reader'
            model = TIFFSeriesReader(registrationName=fileName, FileNames=[inputFile])
            model.UseCustomDataSpacing = 1
            model.CustomDataSpacing = CustomDataSpacing

            # create a new 'Contour'
            contourName = 'Contour ' + fileName[:-4]
            contour = Contour(registrationName=contourName, Input=model)
            contour.ContourBy = ['POINTS', 'Tiff Scalars']
            contour.ComputeGradients = 1
            contour.Isosurfaces = Isosurfaces
            contour.PointMergeMethod = 'Uniform Binning'

            # # save the 'Contour' as .x3d to the output folder
            # x3d = contourName + ".x3d"
            # print(x3d)
            # ExportScene(outputFolder + x3d, View=GetActiveViewOrCreate('RenderView'))

    return inputFiles

# ----------------------------------------------------------------
# output a log file for reproducibility of experiments
# ----------------------------------------------------------------

def WriteLog(logPath, inputFiles, CustomDataSpacing, Isosurfaces):
    # no input file found
    if not inputFiles: return

    # log completed session
    with open(logPath, 'a') as f:
        f.write(f"[{datetime.now()}] PARAVIEW SESSION COMPLETED\n")
        f.write(f"Input Files: \n")
        for input in inputFiles:
            f.write(f"{input}\n")

        # modified parameters
        f.write(f"Custom Data Spacing: {CustomDataSpacing}\n")
        f.write(f"Isosurfaces: {Isosurfaces}\n")

# ----------------------------------------------------------------
# main script execution
# ----------------------------------------------------------------

# currently use an absolute path for the config file
configPath = "/Users/cheryl/Documents/GitHub/AIVE-Intro/ParaviewStreamline/config.json"
InputFolder, OutputFolder, CustomDataSpacing, Isosurfaces = ReadConfigFile(configPath)
inputFiles = ProcessFolder(InputFolder, OutputFolder, CustomDataSpacing, Isosurfaces)
logFilePath = os.path.expanduser("/Users/cheryl/Documents/GitHub/AIVE-Intro/ParaviewStreamline/log.txt")
WriteLog(logFilePath, inputFiles, CustomDataSpacing, Isosurfaces)