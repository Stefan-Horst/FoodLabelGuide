import os
from PIL import Image

# Define the directories
directories = [
    "/home/oguyig00/aiss/aiss_cv_group_6/data/datasets/training_data_augmented_V4_deleted_and_merged",
    "/home/oguyig00/aiss/aiss_cv_group_6/data/datasets/training_data_augmented_V4_deleted_not_merged"
]

# Function to ensure each jpg has a corresponding txt
def ensure_txt_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_filepath = os.path.join(directory, txt_filename)
            if not os.path.exists(txt_filepath):
                # Create an empty txt file if it does not exist
                with open(txt_filepath, 'w') as f:
                    pass

# Function to resize images in negative samples directory
def resize_images(directory, size=(960, 960)):
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            img_path = os.path.join(directory, filename)
            with Image.open(img_path) as img:
                resized_img = img.resize(size)
                resized_img.save(img_path)

# Iterate through each directory
for directory in directories:
    ensure_txt_files(directory)

# Resize images in the negative samples directory
#resize_images("/home/oguyig00/aiss/aiss_cv_group_6/data/datasets/negative_samples")

print("Task completed successfully.")
