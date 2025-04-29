import os

test_path = r'E:/AIVE_main/paraview work/Test for one file in Paraview/A2_Output/MP3_Model5A_06.tif'
if not os.path.exists(test_path):
    print("❌ The file does not exist！")
else:
    print("✅ The file exists！")