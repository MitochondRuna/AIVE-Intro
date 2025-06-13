from paraview.simple import *
import os

# Get all contour sources
all_sources = GetSources()
contour_sources = [key[0] for key in all_sources if key[0].startswith("Contour_")]

if not contour_sources:
    print("No sources found with names starting with 'Contour_'.")
    exit()

print("Available Contour sources:")
for idx, name in enumerate(contour_sources):
    print(f"{idx}: {name}")

# Get user input for source indices (comma separated)
indices_str = input("Enter indices of Contour sources to save (comma separated): ")
indices = [int(i.strip()) for i in indices_str.split(",") if i.strip().isdigit()]

# Get save folder path
save_folder = input("Enter folder path to save STL files: ").strip()
if not save_folder.endswith('/') and not save_folder.endswith('\\'):
    save_folder += '/'

for i in indices:
    if 0 <= i < len(contour_sources):
        name = contour_sources[i]
        source = FindSource(name)
        full_path = os.path.join(save_folder, f"{name}.stl")
        SaveData(full_path, proxy=source)
        print(f"Saved: {full_path}")
    else:
        print(f"Index {i} out of range, skipped.")
