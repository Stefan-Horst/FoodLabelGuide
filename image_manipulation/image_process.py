import os
import cv2


def resize_image(image_path, output_path, size=(960, 960)):
    """
    Resize an image to the given size and save it to the output path.

    :param image_path: Path to the input image
    :param output_path: Path to save the resized image
    :param size: Tuple indicating the new size (width, height)
    """
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, resized_image)


def resize_images_in_directory(input_dir, output_dir, size=(960, 960)):
    """
    Resize all images in a given directory to the specified size and save them
    to an output directory.

    :param input_dir: Path to the directory containing input images
    :param output_dir: Path to the directory to save resized images
    :param size: Tuple indicating the new size (width, height)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(("png", "jpg", "jpeg", "bmp", "gif")):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)

                # Create the output directory structure if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                try:
                    resize_image(input_path, output_path, size)
                    print(f"Resized and saved {file} to {output_path}")
                except Exception as e:
                    print(f"Failed to process {file}: {e}")


if __name__ == "__main__":
    input_directory = "C:/Users/mucki/Downloads/images_without_labels_scheckin_01_06"
    output_directory = (
        "C:/Users/mucki/Downloads/images_without_labels_scheckin_01_06_resized"
    )

    resize_images_in_directory(input_directory, output_directory)
