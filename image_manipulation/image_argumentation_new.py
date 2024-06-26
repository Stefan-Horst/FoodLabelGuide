import os
import albumentations as A
import cv2

# Define a list of augmentation strategies, each combination includes different transformations
transform_strategies = [
    A.Compose([
        A.SafeRotate(limit=180, p=1.0),
        A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2, p=1.0),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['labels'], min_visibility=0.5)),
    
    A.Compose([
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1.0),
        A.RandomSizedBBoxSafeCrop(height=200, width=200, p=1.0),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['labels'], min_visibility=0.5)),
    
    A.Compose([
        A.HorizontalFlip(p=1.0),
        A.GaussianBlur(blur_limit=(3, 7), p=1.0),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['labels'], min_visibility=0.5)),
    
    A.Compose([
        A.VerticalFlip(p=1.0),
        A.ElasticTransform(p=1.0),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['labels'], min_visibility=0.5))
]

# Augmentation strategies without bounding boxes
transform_strategies_no_bbox = [
    A.Compose([
        A.SafeRotate(limit=180, p=1.0),
        A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2, p=1.0),
    ]),
    
    A.Compose([
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1.0),
        A.CenterCrop(height=200, width=200, p=1.0),
    ]),
    
    A.Compose([
        A.HorizontalFlip(p=1.0),
        A.GaussianBlur(blur_limit=(3, 7), p=1.0),
    ]),
    
    A.Compose([
        A.VerticalFlip(p=1.0),
        A.ElasticTransform(p=1.0),
    ])
]

def read_yolo_labels(label_path):
    labels = []
    bboxes = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                labels.append(int(parts[0]))
                bboxes.append([float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])])
    return labels, bboxes

def write_yolo_labels(label_path, labels, bboxes):
    with open(label_path, 'w') as f:
        for label, bbox in zip(labels, bboxes):
            f.write(f"{label} {' '.join(map(str, bbox))}\n")

def process_images(image_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_file in os.listdir(image_dir):
        if not image_file.endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        image_path = os.path.join(image_dir, image_file)
        label_path = os.path.splitext(image_path)[0] + '.txt'
        
        labels, bboxes = read_yolo_labels(label_path)
        
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if labels:
            for i, transform in enumerate(transform_strategies):
                transformed = transform(image=image, bboxes=bboxes, labels=labels)
                transformed_image = transformed["image"]
                transformed_bboxes = transformed["bboxes"]

                # Save the augmented image
                transformed_image_path = os.path.join(output_dir, f"{os.path.splitext(image_file)[0]}_aug_{i+1}.jpg")
                cv2.imwrite(transformed_image_path, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))

                # Save the updated label file
                transformed_label_path = os.path.splitext(transformed_image_path)[0] + '.txt'
                write_yolo_labels(transformed_label_path, labels, transformed_bboxes)
        else:
            for i, transform in enumerate(transform_strategies_no_bbox):
                transformed = transform(image=image)
                transformed_image = transformed["image"]

                # Save the augmented image
                transformed_image_path = os.path.join(output_dir, f"{os.path.splitext(image_file)[0]}_aug_{i+1}.jpg")
                cv2.imwrite(transformed_image_path, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))

# Example call
input_dir = 'C:/Users/Felix/Documents/00_Master/03_SS-24/10_AISS_CV/datasets/training_data_complete'
output_dir = 'C:/Users/Felix/Documents/00_Master/03_SS-24/10_AISS_CV/datasets/training_data_augmented_V2'
process_images(input_dir, output_dir)
