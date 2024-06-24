import os
import glob
import cv2
import albumentations as A

# Define the augmentation pipeline
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),
    A.Blur(blur_limit=3, p=0.2),
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.2, rotate_limit=45, p=0.5),
    A.CLAHE(p=0.2)
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

# Paths
input_dir = 'C:/Users/Felix/Documents/00_Master/03_SS-24/10_AISS_CV/datasets/training_data_complete'
output_dir = 'C:/Users/Felix/Documents/00_Master/03_SS-24/10_AISS_CV/datasets/training_data_augmented'
output_dir_positive = os.path.join(output_dir, 'positive')
output_dir_negative = os.path.join(output_dir, 'negative')

if not os.path.exists(output_dir_positive):
    os.makedirs(output_dir_positive)
if not os.path.exists(output_dir_negative):
    os.makedirs(output_dir_negative)

# Get all image files
image_files = glob.glob(os.path.join(input_dir, '*.jpg'))  # Change extension if different

# Process each image
for image_path in image_files:
    # Read image
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Get corresponding label file
    label_path = image_path.replace('.jpg', '.txt')
    
    if not os.path.exists(label_path):
        # Save the image without labels in the negative folder
        output_image_path = os.path.join(output_dir_negative, os.path.basename(image_path))
        cv2.imwrite(output_image_path, image)
        continue

    # Read labels
    with open(label_path, 'r') as f:
        labels = f.readlines()

    if not labels:
        # Save the image without labels in the negative folder
        output_image_path = os.path.join(output_dir_negative, os.path.basename(image_path))
        cv2.imwrite(output_image_path, image)
        continue

    # Parse labels
    bboxes = []
    class_labels = []
    for label in labels:
        class_id, x_center, y_center, bbox_width, bbox_height = map(float, label.strip().split())
        bboxes.append([x_center, y_center, bbox_width, bbox_height])
        class_labels.append(class_id)

    # Apply augmentations
    augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)
    augmented_image = augmented['image']
    augmented_bboxes = augmented['bboxes']
    augmented_class_labels = augmented['class_labels']

    # Save augmented image
    output_image_path = os.path.join(output_dir_positive, os.path.basename(image_path))
    cv2.imwrite(output_image_path, augmented_image)

    # Save augmented labels
    output_label_path = output_image_path.replace('.jpg', '.txt')
    with open(output_label_path, 'w') as f:
        for bbox, class_id in zip(augmented_bboxes, augmented_class_labels):
            f.write(f"{int(class_id)} {' '.join(map(str, bbox))}\n")

print("Data augmentation complete.")
