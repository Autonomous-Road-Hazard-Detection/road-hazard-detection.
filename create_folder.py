import os

folders = [
"dataset/images/train",
"dataset/images/val",
"dataset/labels/train",
"dataset/labels/val"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("Folders created successfully!")