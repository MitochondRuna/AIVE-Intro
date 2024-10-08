# Library imports
from tkinter import Tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import cv2
import os

# Constant definitions
ERROR = -1  # Error flag
INIT_N = 0  # Initial number
INIT_I = 0  # Initial index

def image_select():
    """
    Opens dialog to select image file

    :return: Filepath of selected image file
    """

    root = Tk()
    root.withdraw()  # Hide root window
    filepath = filedialog.askopenfilename(title="Select image file")
    return filepath


def mask_dir_select():
    """
    Opens dialog to select masks' output directory

    :return: Masks' output directory
    """

    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select masks' output directory")
    return directory


def load_image_stack(image_path):
    """
    Load multi-page TIFF image stack

    :param image_path: Image file path
    :return: Image stack as list of NumPy arrays
    """

    # Open image and initialise empty image stack
    image = Image.open(image_path)
    image_stack = []

    # Load each frame in image into stack
    try:
        while True:
            frame = np.array(image)
            image_stack.append(frame)
            image.seek(image.tell() + 1)  # Move to next frame
    except EOFError:
        pass

    return image_stack


def threshold_apply(image, threshold):
    """
    Applies threshold to image to create binary mask

    :param image: Image as NumPy array
    :param threshold: Unique pixel value
    :return: Mask as NumPy array
    """

    mask = cv2.inRange(image, np.array(threshold), np.array(threshold))
    return mask


def mask_stack_save(mask_stack, mask_stack_path):
    """
    Save mask stack at specified path

    :param mask_stack: Mask stack as list of NumPy arrays
    :param mask_stack_path: Mask stack file path
    """

    mask_image_stack = [Image.fromarray(mask) for mask in mask_stack]  # Convert
    # mask stack from NumPy arrays into images
    mask_image_stack[INIT_I].save(mask_stack_path, save_all=True,
                                  append_images=mask_image_stack[INIT_I + 1:],
                                  compression="tiff_deflate")  # Save mask stack
    # at specified path


def image_split(image_path, mask_dir, mask_prefix):
    """
    Splits image into binary masks based on unique pixel values

    :param image_path: Image file path
    :param mask_dir: Masks' output directory
    :param mask_prefix: Masks' filename prefix
    """

    image_stack = load_image_stack(image_path)  # Load image stack (32-bit TIFF
    # image)
    if len(image_stack) == INIT_N:
        print("Image stack load failed")
        return ERROR

    unique_values = np.unique(image_stack)  # Get unique pixel values in image
    # stack

    # Create mask using each unique pixel value
    for value in unique_values:
        if value == INIT_N:  # If value==0 resulting mask will be inverted image
            # therefore skip
            continue

        mask_stack = []
        for image_slice in image_stack: # Apply threshold to each slice in image
            # stack
            mask = threshold_apply(image_slice, value)
            mask_stack.append(mask)

        # Save mask stack
        index = f"{value:02d}"  # Add leading zero for single-digit indices
        mask_stack_path = os.path.join(mask_dir, f"{mask_prefix}_{index}.tif")
        mask_stack_save(mask_stack, mask_stack_path)
        print(f"Mask stack saved: {mask_stack_path}")


def main():
    """'macro1' splits MIB models into binary masks"""

    image_path = image_select()  # Select image file
    if image_path=="":
        print("No image selected")
        return ERROR
    elif not image_path.endswith(".tif"):
        print("Invalid image file format ('.tif' required)")
        return ERROR

    mask_prefix = input("Enter masks' filename prefix (default (blank) is "
                        "'default'): ") or "default"  # Enter masks' filename
    # prefix
    mask_dir = mask_dir_select()  # Select masks' output directory
    image_split(image_path, mask_dir, mask_prefix)  # Split image into masks


if __name__ == "__main__":
    main()