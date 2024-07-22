import os
import random
from collections import defaultdict, Counter
from sklearn.model_selection import train_test_split

# Set paths
data_path = '/home/oguyig00/aiss/aiss_cv_group_6/data/datasets/training_data_augmented_V4_deleted_and_merged'
image_files = [os.path.join(data_path, f) for f in os.listdir(data_path) if f.endswith('.jpg')]
annotation_files = [f.replace('.jpg', '.txt') for f in image_files]

# Read annotations and count occurrences of each class
class_counts = Counter()
image_annotations = []

for image_file, annotation_file in zip(image_files, annotation_files):
    with open(annotation_file, 'r') as f:
        lines = f.readlines()
        if lines:
            classes = [int(line.split()[0]) for line in lines]
            class_counts.update(classes)
        else:
            classes = []  # Empty .txt indicates a negative sample
        image_annotations.append((image_file, classes))

# Sort classes by their counts (ascending)
sorted_classes = [cls for cls, _ in class_counts.most_common()[::-1]]

# Group images by class occurrence and split them
train_files, valid_files, test_files = [], [], []

for cls in sorted_classes:
    cls_images = [img for img, classes in image_annotations if cls in classes]
    train, temp = train_test_split(cls_images, test_size=0.3, random_state=42)
    valid, test = train_test_split(temp, test_size=0.5, random_state=42)
    train_files.extend(train)
    valid_files.extend(valid)
    test_files.extend(test)

# Include negative samples
negative_samples = [img for img, classes in image_annotations if not classes]
train_neg, temp_neg = train_test_split(negative_samples, test_size=0.3, random_state=42)
valid_neg, test_neg = train_test_split(temp_neg, test_size=0.5, random_state=42)
train_files.extend(train_neg)
valid_files.extend(valid_neg)
test_files.extend(test_neg)

# Write file paths to respective .txt files
with open('train.txt', 'w') as f:
    for file in train_files:
        f.write(f"{file}\n")

with open('valid.txt', 'w') as f:
    for file in valid_files:
        f.write(f"{file}\n")

with open('test.txt', 'w') as f:
    for file in test_files:
        f.write(f"{file}\n")