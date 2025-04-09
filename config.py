import configparser

# Define parameters
x = "_02"  # Suffix that can be changed for the file
registration_name = 'Model5A' + x  # Registration name for the image
file_path = r'E:\AIVE_main\intern work\A2_Output\MP3_Model5A' + x + '.tif'  # File path for the TIFF file
custom_data_spacing = [0.030013, 0.030013, 0.1]  # Custom data spacing values
contour_isosurface_value = 48.0  # Isosurface value for contour

# Create a configuration object
config = configparser.ConfigParser()

# Add the section 'GENERAL' if it doesn't exist
config.add_section('GENERAL')

# Set configuration parameters
config.set('GENERAL', 'registration_name', registration_name)  # Set the registration name
config.set('GENERAL', 'file_path', file_path)  # Set the file path

# Set the custom data spacing, converting the list to a string
config.set('GENERAL', 'custom_data_spacing', ','.join(map(str, custom_data_spacing)))  # Set data spacing
config.set('GENERAL', 'contour_isosurface_value', str(contour_isosurface_value))  # Set the contour isosurface value

# Write the configuration to a file
with open('config.ini', 'w') as configfile:
    config.write(configfile)
