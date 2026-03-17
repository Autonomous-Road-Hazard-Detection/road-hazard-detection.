import os
import shutil

# Path where ExDark images are located
source_dir = r"C:\Users\chinn\Downloads\ex-dark dataset extracted"

# Destination folder in your project
destination_dir = r"C:\Users\chinn\road-hazard\dataset\images\train"

os.makedirs(destination_dir, exist_ok=True)

# Supported image formats
image_extensions = (".jpg", ".jpeg", ".png")

count = 0

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith(image_extensions):
            src_file = os.path.join(root, file)
            dst_file = os.path.join(destination_dir, file)

            shutil.copy(src_file, dst_file)
            count += 1

print(f"{count} images copied successfully!")