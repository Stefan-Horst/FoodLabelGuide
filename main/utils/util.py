import os
import re
import json
from pathlib import Path
from utils.globals import *


# Use to get most recent model output file in respective directory
def get_newest_file_in_dir(dir_path):
    file_paths = sorted(Path(dir_path).iterdir(), key=os.path.getmtime)
    if len(file_paths) > 0:
        return file_paths[-1]
    else:
        return ""


# Read yolo model output file and return predicted labels with bounding boxes as a dict
def read_yolo_output(file_name):
    path = DIR_MODEL_RESULTS / file_name
    file = open(path, "r")
    lines = file.readlines()

    labels = []
    for i in range(len(lines)):
        line = lines[-i-1]
        if "%\t" in line:
            labels.append(line)

    # Dict structure: {"label_name": [confidence_percent, left_x, top_y, width, height]}
    labels_dict = {}
    for label in labels:
        splits = label.split(":", 1)
        if len(splits) != 2:
            print("WARNING: abnormal label", splits)

        name = splits[0]
        data = splits[1]

        num_list = [int(s) for s in re.findall("-?\d+\.?\d*", data)] # Regex for all numbers
        if len(num_list) != 5:
            print("WARNING: abnormal label data", num_list)
        
        labels_dict[name] = num_list

    return labels_dict


# Read json file containing label info and return it as dict
def read_label_dict(file_name):
    path_dict = DIR_RESOURCES / file_name
    with open(path_dict, "r", encoding="utf-8") as file:
        dict = json.load(file)
    
    return dict


# Get data for specific label dict entry by label name
def get_label_data(label_name, dict):
    for label, val in dict.items():
        name = val["name"]
        description = val["description"]
        img_file_name = val["img_path"]
        #img_path = DIR_IMG / img_file_name # absolute path
        img_path = DIR_IMG_REL + img_file_name

        if label == label_name:
            return img_path, name, description
    return
