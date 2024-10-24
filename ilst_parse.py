import sys
import xml.etree.ElementTree as ET
from glob import glob

def convert_to_yolo_format(xml_file, class_mapping):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Image dimensions
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)
    
    if width <=0 or height <=0:
        print ("Size not found")
        return []

    # To store YOLO formatted results
    yolo_data = []

    # Iterate over all objects in the XML
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        
        # Get class ID from the class_mapping
        #class_id = class_mapping.get(class_name, -1)
        class_id = 0
        if class_id == -1:
            raise ValueError(f"Class {class_name} not found in class mapping")
        
        # Bounding box coordinates
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)

        # Calculate YOLO format values
        x_center = (xmin + xmax) / 2.0 / width
        y_center = (ymin + ymax) / 2.0 / height
        box_width = (xmax - xmin) / width
        box_height = (ymax - ymin) / height

        # Append in YOLO format: class_id, x_center, y_center, box_width, box_height
        yolo_data.append(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}")

    return yolo_data

# Example usage
class_mapping = {
}


all_files = glob("*.xml")

for xml_file in all_files:
    print (xml_file)
        
    yolo_annotations = convert_to_yolo_format(xml_file, class_mapping)

    out_file = xml_file.replace(".xml", ".txt")
    for annotation in yolo_annotations:
        #print(annotation)
        with open(out_file, 'a') as file:
            file.write(annotation + '\n')

