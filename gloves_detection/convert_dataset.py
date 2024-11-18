import os
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(xml_folder, image_folder, output_folder, class_names):
    os.makedirs(output_folder, exist_ok=True)
    
    for xml_file in os.listdir(xml_folder):
        if not xml_file.endswith(".xml"):
            continue
        
        tree = ET.parse(os.path.join(xml_folder, xml_file))
        root = tree.getroot()
        
        filename = root.find('filename').text
        image_width = int(root.find('size/width').text)
        image_height = int(root.find('size/height').text)
        
        yolo_annotations = []
        
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name not in class_names:
                continue
            
            class_id = class_names.index(class_name)
            bndbox = obj.find('bndbox')
            
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)
            
            # Convert to YOLO format
            x_center = (xmin + xmax) / 2 / image_width
            y_center = (ymin + ymax) / 2 / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height
            
            yolo_annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")
        
        # Save YOLO annotations to a file
        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".txt")
        with open(output_file, 'w') as f:
            f.write("\n".join(yolo_annotations))

# Example usage
xml_folder = "yolo_gloves/datasets_change/Annotations/Annotations"
image_folder = "yolo_gloves/datasets_change/palm_300"
output_folder = "yolo_gloves/datasets"
class_names = ["human_palm"]  # Add more class names if needed

convert_voc_to_yolo(xml_folder, image_folder, output_folder, class_names)
