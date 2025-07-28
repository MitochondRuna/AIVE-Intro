import configparser

# Define parameters
folder_path = r"E:\AIVE_main\paraview work\Test for one file in Paraview\A2_Output\\"
file_prefix = "MP3_Model5A"  # File name prefix, before "_01", etc.
registration_prefix = "Model5A"
custom_data_spacing = [0.030013, 0.030013, 0.1]
contour_isosurface_value = 48.0

# Create a configuration object
config = configparser.ConfigParser()

# Add the section 'GENERAL' if it doesn't exist
config.add_section('GENERAL')

# Set configuration parameters
config.set('GENERAL', 'folder_path', folder_path) 
config.set('GENERAL', 'ffile_prefix', file_prefix) 
config.set('GENERAL', 'registration_prefix',registration_prefix)

# Set the custom data spacing, converting the list to a string
config.set('GENERAL', 'custom_data_spacing', ','.join(map(str, custom_data_spacing)))  # Set data spacing
config.set('GENERAL', 'contour_isosurface_value', str(contour_isosurface_value))  # Set the contour isosurface value

# Write the configuration to a file
with open('config_for_multiple_files.ini', 'w') as configfile:
    config.write(configfile)
