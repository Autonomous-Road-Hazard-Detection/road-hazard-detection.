import os
import shutil

image_train = "dataset/images/train"
image_val = "dataset/images/val"

label_source = "dataset/labels"

label_train = "dataset/labels/train"
label_val = "dataset/labels/val"

os.makedirs(label_train, exist_ok=True)
os.makedirs(label_val, exist_ok=True)

# copy labels for train images
for img in os.listdir(image_train):
    name = os.path.splitext(img)[0] + ".txt"
    src = os.path.join(label_source, name)
    dst = os.path.join(label_train, name)

    if os.path.exists(src):
        shutil.copy(src, dst)

# copy labels for val images
for img in os.listdir(image_val):
    name = os.path.splitext(img)[0] + ".txt"
    src = os.path.join(label_source, name)
    dst = os.path.join(label_val, name)

    if os.path.exists(src):
        shutil.copy(src, dst)

print("Labels distributed successfully!")