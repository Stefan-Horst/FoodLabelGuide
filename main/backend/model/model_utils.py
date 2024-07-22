import os
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

# Loading darknet config and weights
network, class_names, class_colors = darknet.load_network(
    str(DIR_MODEL_DATA / "yolov4-tiny-labeldetector.cfg"),
    str(DIR_MODEL_DATA / "obj.data"),
    str(DIR_MODEL_DATA / "yolov4-tiny-labeldetector-alldata.weights")
)

width = darknet.network_width(network)
height = darknet.network_height(network)


def convert_to_darknet_image(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height), interpolation=cv2.INTER_LINEAR)
    darknet_image = darknet.make_image(width, height, 3)
    darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
    return darknet_image


def detect_image(image, save_file=True, file_dir=DIR_WEB_RESULT_IMG, file_name="result"):
	frame = cv2.imread(str(image))
	darknet_image = convert_to_darknet_image(frame)
	# Detection
	detections = darknet.detect_image(network, class_names, darknet_image)
	darknet.free_image(darknet_image)
	if save_file:
		global image_counter
		# Draw bbs
		image = darknet.draw_boxes(detections, frame, class_colors)
		path = file_dir / (file_name + str(image_counter) + ".jpg")
		cv2.imwrite(str(path), image)
		image_counter = image_counter + 1
	return detections
