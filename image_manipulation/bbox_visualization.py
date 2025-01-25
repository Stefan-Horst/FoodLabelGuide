import cv2
import matplotlib.pyplot as plt

BOX_COLOR = (255, 0, 0)  # Red
TEXT_COLOR = (255, 255, 255)  # White

def visualize_bbox(img, bbox, class_name, color=BOX_COLOR, thickness=2):
    """Visualizes a single bounding box on the image."""
    x_min, y_min, w, h = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)

    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(
        img,
        text=class_name,
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35,
        color=TEXT_COLOR,
        lineType=cv2.LINE_AA,
    )
    return img

def visualize(image_path, label_path, classes_path):
    """Visualizes an image with its labeled bounding boxes."""
    # Load image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Read labels
    with open(label_path, 'r') as f:
        labels = f.readlines()

    # Parse classes
    with open(classes_path, 'r') as f:
        class_names = f.readlines()
    class_names = [name.strip() for name in class_names]

    # Visualize bounding boxes
    for label in labels:
        class_id, x_center, y_center, bbox_width, bbox_height = map(float, label.strip().split())
        class_name = class_names[int(class_id)]

        # Convert YOLO format to (x_min, y_min, width, height)
        x_min = (x_center - bbox_width / 2) * image.shape[1]
        y_min = (y_center - bbox_height / 2) * image.shape[0]
        bbox_width = bbox_width * image.shape[1]
        bbox_height = bbox_height * image.shape[0]

        image = visualize_bbox(image, (x_min, y_min, bbox_width, bbox_height), class_name)

    # Plot image
    plt.figure(figsize=(12, 12))
    plt.imshow(image)
    plt.axis('off')
    plt.show()


# Example usage:
image_path = "../datasets/training_data_augmented/positive/IMG_20240515_175800.jpg"
label_path = "../datasets/training_data_augmented/positive/IMG_20240515_175800.txt"
classes_path = "../datasets/training_data_complete/classes.txt"

visualize(image_path, label_path, classes_path)
