import os
import random
from PIL import Image, ImageEnhance, ImageOps
#import numpy as np

def load_labels(label_path):
    with open(label_path, 'r') as file:
        labels = file.readlines()
    return [label.strip() for label in labels]

def save_labels(labels, label_path):
    with open(label_path, 'w') as file:
        for label in labels:
            file.write(f"{label}\n")

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def adjust_saturation(image, factor):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def flip_image(image, labels, direction='horizontal'):
    if direction == 'horizontal':
        image = ImageOps.mirror(image)
        flipped_labels = []
        for label in labels:
            class_id, x_center, y_center, width, height = map(float, label.split())
            x_center = 1.0 - x_center
            flipped_labels.append(f"{class_id} {x_center} {y_center} {width} {height}")
    else:  # vertical flip
        image = ImageOps.flip(image)
        flipped_labels = []
        for label in labels:
            class_id, x_center, y_center, width, height = map(float, label.split())
            y_center = 1.0 - y_center
            flipped_labels.append(f"{class_id} {x_center} {y_center} {width} {height}")
    return image, flipped_labels

def augment_image(image, labels, output_dir, filename):
    operations = [
        ('brightness', adjust_brightness, random.uniform(0.5, 1.5)),
        ('contrast', adjust_contrast, random.uniform(0.5, 1.5)),
        ('saturation', adjust_saturation, random.uniform(0.5, 1.5)),
        ('flip_h', flip_image, 'horizontal'),
        ('flip_v', flip_image, 'vertical')
    ]
    random.shuffle(operations)

    for operation_name, operation, factor in operations:
        augmented_image = image.copy()
        augmented_labels = labels.copy()
        if 'flip' in operation_name:
            augmented_image, augmented_labels = operation(augmented_image, augmented_labels, factor)
        else:
            augmented_image = operation(augmented_image, factor)
        
        augmented_filename = f"{filename.split('.')[0]}_{operation_name}.jpg"
        augmented_label_filename = f"{filename.split('.')[0]}_{operation_name}.txt"

        augmented_image.save(os.path.join(output_dir, augmented_filename))
        save_labels(augmented_labels, os.path.join(output_dir, augmented_label_filename))

def main(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_dir, filename)
            label_path = os.path.join(input_dir, filename.split('.')[0] + ".txt")
            
            image = Image.open(image_path)
            labels = load_labels(label_path)
            
            augment_image(image, labels, output_dir, filename)

if __name__ == "__main__":
    input_dir = '../resized'
    output_dir = '../augmented'
    main(input_dir, output_dir)
