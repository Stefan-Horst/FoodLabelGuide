import cv2
import backend.model.darknet as darknet
from utils.globals import *


# create obj.data file for darknet, use absolute paths based on current dir
obj_data = ("classes = 26\n"
		   	f"train = {str(DIR_MODEL)}/data/train.txt\n"
			f"valid = {str(DIR_MODEL)}/data/test.txt\n"
		 	f"names = {str(DIR_MODEL)}/data/classes.txt\n"
			f"backup = {str(DIR_MODEL)}/data/backup/")

with open(DIR_MODEL / "data/obj.data", "w") as f:
	f.write(obj_data)

# file name counter for saved images
image_counter = 0

# cache image from current detection so it can be saved by other function
current_detections = []
current_image = []

# Loading darknet config and weights
network, class_names, class_colors = darknet.load_network(
    str(DIR_MODEL_DATA / "yolov4-tiny-labeldetector.cfg"),
    str(DIR_MODEL_DATA / "obj.data"),
    str(DIR_MODEL_DATA / "yolov4-tiny-labeldetector-alldata.weights")
)

# 960x960
width = darknet.network_width(network)
height = darknet.network_height(network)


# transform image to same dimensions as model expects as input
def preprocess_image(frame):
	fheight, fwidth, _ = frame.shape

	# crop landscape format image by cutting left and right sides to make it square (like model input)
	margin = int((fwidth - fheight) / 2)
	frame_cropped = frame[:, margin:fwidth-margin]

	# use same (size) image for model input and to save with bboxes so bboxes are at correct position
	frame_resized = cv2.resize(frame_cropped, (width, height), interpolation=cv2.INTER_LINEAR)
	return frame_resized


def convert_to_darknet_image(frame, preprocess=True):
	if preprocess:
		frame = preprocess_image(frame)
	else:
		fheight, fwidth, _ = frame.shape
		if fheight != height or fwidth != width:
			print("model_utils: error - wrong image size")
			return

	global current_image
	current_image = frame

	frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	darknet_image = darknet.make_image(width, height, 3)
	darknet.copy_image_from_bytes(darknet_image, frame_rgb.tobytes())
	return darknet_image


# return predicted labels and bounding box coordinates for given image or path to image
def detect_image(image, type="path"):
	if type == "path":
		frame = cv2.imread(str(image))
	elif type == "file":
		frame = image
	else:
		print("model_utils: error - wrong image type")
		return
	
	darknet_image = convert_to_darknet_image(frame)

	# Detection
	detections = darknet.detect_image(network, class_names, darknet_image)
	darknet.free_image(darknet_image)

	global current_detections
	current_detections = detections

	return detections


def draw_bounding_boxes(detections, image):
	bb_image = darknet.draw_boxes(detections, image, class_colors)
	return bb_image


def save_current_image(file_dir=DIR_WEB_RESULT_IMG, file_name="result"):
	if len(current_image) != 0: # check if image exists
		global image_counter
		# Draw bounding boxes
		path = file_dir / (file_name + str(image_counter) + ".jpg")
		bb_image = draw_bounding_boxes(current_detections, current_image)
		cv2.imwrite(str(path), bb_image)
		image_counter = image_counter + 1
	return
