import xml.etree.ElementTree as ET
import os

# Classes we want
classes = ["car", "bus", "truck", "bicycle", "person", "motorbike"]

annotations_path = "ExDark/annotations"
labels_train = "dataset/labels/train"
labels_val = "dataset/labels/val"

os.makedirs(labels_train, exist_ok=True)
os.makedirs(labels_val, exist_ok=True)

def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]

    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0

    w = box[1] - box[0]
    h = box[3] - box[2]

    return (x * dw, y * dh, w * dw, h * dh)


for xml_file in os.listdir(annotations_path):

    tree = ET.parse(os.path.join(annotations_path, xml_file))
    root = tree.getroot()

    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    filename = root.find("filename").text
    label_file = filename.replace(".jpg", ".txt")

    if os.path.exists(f"dataset/images/train/{filename}"):
        label_path = os.path.join(labels_train, label_file)
    else:
        label_path = os.path.join(labels_val, label_file)

    with open(label_path, "w") as f:

        for obj in root.iter("object"):
            cls = obj.find("name").text

            if cls not in classes:
                continue

            cls_id = classes.index(cls)

            xmlbox = obj.find("bndbox")
            b = (
                float(xmlbox.find("xmin").text),
                float(xmlbox.find("xmax").text),
                float(xmlbox.find("ymin").text),
                float(xmlbox.find("ymax").text),
            )

            bb = convert((w, h), b)

            f.write(str(cls_id) + " " + " ".join(map(str, bb)) + "\n")

print("Annotations converted to YOLO format!")