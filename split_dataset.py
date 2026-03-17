import os
import shutil

base = "dataset"

# create required structure
os.makedirs("dataset/images/train", exist_ok=True)
os.makedirs("dataset/images/val", exist_ok=True)
os.makedirs("dataset/labels/train", exist_ok=True)
os.makedirs("dataset/labels/val", exist_ok=True)

# move train images
for file in os.listdir("dataset/train/images"):
    shutil.move(f"dataset/train/images/{file}", f"dataset/images/train/{file}")

# move train labels
for file in os.listdir("dataset/train/labels"):
    shutil.move(f"dataset/train/labels/{file}", f"dataset/labels/train/{file}")

# move val images
for file in os.listdir("dataset/val/images"):
    shutil.move(f"dataset/val/images/{file}", f"dataset/images/val/{file}")

# move val labels
for file in os.listdir("dataset/val/labels"):
    shutil.move(f"dataset/val/labels/{file}", f"dataset/labels/val/{file}")

print("Dataset structure fixed successfully!")