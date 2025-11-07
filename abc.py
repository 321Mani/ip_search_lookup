#!/usr/bin/python3
# import os
# import sys

# path = os.path.realpath(os.path.dirname(sys.argv[0]))
# print(path)

# from PIL import Image
# from pathlib import Path

# # Path to the specific image file (WoodenTable_1.png)
# img_path = Path('./static/Images/PTRCWQ5NNQYCJGQZ.jpeg')

# # Check if the image exists and is in PNG format
# if img_path.exists() and img_path.suffix.lower() == '.jpeg':
#     try:
#         # Open the PNG image
#         img = Image.open(img_path)

#         # Convert to RGB (necessary for PNG to JPG conversion)
#         img = img.convert('RGB')

#         # Define the new image path (save as .jpg)
#         new_img_path = img_path.with_suffix('.jpg')

#         # Save the image as JPG
#         img.save(new_img_path, 'JPEG')

#         print(f"Converted {img_path.name} to {new_img_path.name}")

#     except Exception as e:
#         print(f"Error converting {img_path.name}: {e}")
# else:
#     print("The file WoodenTable_1.png does not exist or is not in PNG format.")

# import os
# from PIL import Image
# from pathlib import Path

# # Path to the directory containing the images
# image_dir = Path('./static/Images')

# # Loop through all files in the directory
# for img_path in image_dir.glob('*'):  # Using glob to match all files in the directory
#     # Check if the file is a .jpeg or .png
#     if img_path.suffix.lower() in ['.jpeg', '.png']:
#         try:
#             # Open the image
#             img = Image.open(img_path)

#             # Convert to RGB (needed for PNG to JPG conversion)
#             img = img.convert('RGB')

#             # Define the new path with a .jpg extension
#             new_img_path = img_path.with_suffix('.jpg')

#             # Save the image in .jpg format
#             img.save(new_img_path, 'JPEG')

#             print(f"Converted {img_path.name} to {new_img_path.name}")

#         except Exception as e:
#             print(f"Error converting {img_path.name}: {e}")

import os
from PIL import Image
from pathlib import Path

# Path to the directory containing the images
image_dir = Path('./static/Images')

# Loop through all files in the directory
for img_path in image_dir.glob('*'):
    # Skip files that are already .jpg
    if img_path.suffix.lower() == '.jpg':
        continue  # Ignore already converted files

    # Check if the file is a .jpeg or .png
    if img_path.suffix.lower() in ['.jpeg', '.png', '.webp']:
        try:
            # Define the new path with a .jpg extension
            new_img_path = img_path.with_suffix('.jpg')

            # Skip conversion if the JPG file already exists
            if new_img_path.exists():
                print(f"Skipping {img_path.name}, already converted.")
                continue

            # Open the image
            img = Image.open(img_path)

            # Convert to RGB (needed for PNG to JPG conversion)
            img = img.convert('RGB')

            # Save the image in .jpg format
            img.save(new_img_path, 'JPEG')

            print(f"Converted {img_path.name} to {new_img_path.name}")

        except Exception as e:
            print(f"Error converting {img_path.name}: {e}")
