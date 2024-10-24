import os
from glob import glob
import cv2

def plot_yolo_bboxes(image_path, annotation_path, class_mapping, out_file):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Read YOLO annotation file
    with open(annotation_path, 'r') as file:
        for line in file.readlines():
            class_id, x_center, y_center, box_width, box_height = map(float, line.strip().split())

            # Convert YOLO format back to pixel coordinates
            x_center = x_center * width
            y_center = y_center * height
            box_width = box_width * width
            box_height = box_height * height

            # Calculate the top-left corner of the bounding box
            xmin = int(x_center - (box_width / 2))
            ymin = int(y_center - (box_height / 2))
            xmax = int(x_center + (box_width / 2))
            ymax = int(y_center + (box_height / 2))

            # Draw the bounding box as a rectangle (red, thickness=2)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)

            # Add class label above the bounding box
            class_name = '0'
            cv2.putText(image, class_name, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imwrite(out_file, image)



print ("Start")
images1 = glob("*.jpg")
images2 = glob("*.jpeg")

images = images1 + images2

for image_path in images:
    if "_out.j" in image_path:
        continue
    #image_path = '100.jpg'
    annotation_path = ''
    out_file = "out.jpg"
    if ".jpeg" in image_path:
        annotation_path = image_path.replace(".jpeg", ".txt")
        out_file = image_path.replace(".jpeg", "_out.jpeg")
    else:
        annotation_path = image_path.replace(".jpg", ".txt")
        out_file = image_path.replace(".jpg", "_out.jpg")

    class_mapping = {0: 'പേരൂർ', 1: 'ശ്രീകൃഷ്ണസ്വാമി', 2: 'ക്ഷേത്രം'}

    if os.path.exists(annotation_path):
        plot_yolo_bboxes(image_path, annotation_path, class_mapping, out_file)

