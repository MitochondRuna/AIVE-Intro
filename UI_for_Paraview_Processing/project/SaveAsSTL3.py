from paraview.simple import *
import os

# Get all available sources
all_sources = GetSources()

# Filter sources that start with "Contour_"
contour_sources = [key[0] for key in all_sources if key[0].startswith("Contour_")]

# If no Contour sources found
if not contour_sources:
    print("No sources found with names starting with 'Contour_'.")
    exit()

# Show available options to the user
print("Available Contour sources to save:")
for name in contour_sources:
    print(f"  - {name}")

# Let the user input which ones to save
user_input = input("Enter the names of the Contour sources you want to save (comma-separated, e.g., Contour_01,Contour_04):\n")

# Clean up input
selected_names = [name.strip() for name in user_input.split(",")]

# Ask for the save directory
save_folder = input("Enter the folder path where you want to save the files (e.g., E:/your_folder/):\n").strip()
if not save_folder.endswith('/') and not save_folder.endswith('\\'):
    save_folder += '/'

# Save selected sources
for name in selected_names:
    if name in contour_sources:
        source = FindSource(name)
        filename = f"{name}.stl"
        full_path = os.path.join(save_folder, filename)
        SaveData(full_path, proxy=source)
        print(f"Saved: {full_path}")
    else:
        print(f"[Skipped] Source not found: {name}")
