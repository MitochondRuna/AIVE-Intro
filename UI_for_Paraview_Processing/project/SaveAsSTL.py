from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()
for name in ['Contour_01', 'Contour_03', 'Contour_04']:
    obj = FindSource(name)
    if obj:
        SetActiveSource(obj)
        SaveData(f'E:\AIVE_main\paraview work\Test for one file in Paraview\Project Part 1\New Folder\data.stl', proxy=obj)