import os
import cv2
import backend.model.darknet as darknet
from utils.globals import *


#Loading darknet config and weights
network, class_names, class_colors = darknet.load_network(
    str(DIR_MODEL_CFG / "yolov4-tiny-labeldetector.cfg"),
    str(DIR_MODEL_CFG / "obj.data"),
    str(DIR_MODEL_CFG / "yolov4-tiny-labeldetector-alldata.weights")
)

width = darknet.network_width(network)
height = darknet.network_height(network)

def convert_to_darknet_image(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height), interpolation=cv2.INTER_LINEAR)
    darknet_image = darknet.make_image(width, height, 3)
    darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
    return darknet_image

def detect_image(image):
	frame = cv2.imread(str(image))
	darknet_image = convert_to_darknet_image(frame)
	#Detection
	detections = darknet.detect_image(network, class_names, darknet_image)
	darknet.free_image(darknet_image)
	#Draw bbs
	image = darknet.draw_boxes(detections, frame, class_colors)
	cv2.imwrite(os.path.join(os.getcwd(), DIR_MODEL_RESULTS / "result.jpg"), image)
	return detections

