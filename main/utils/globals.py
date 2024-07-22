from pathlib import Path

def get_root_path(project_folder):
    current_path = Path().resolve()
    path = current_path
    for p in current_path.parents:
        if project_folder not in str(p):
            return path
        path = p

PROJECT_FOLDER = "main"
root_path = get_root_path(PROJECT_FOLDER)


DIR_GUI = root_path / "gui"
DIR_RESOURCES = root_path / "gui/resources"
DIR_BACKEND = root_path / "backend"
DIR_MODEL = root_path / "backend/model"
DIR_MODEL_DATA = root_path / "backend/model/data"
DIR_UTIL = root_path / "util"
DIR_MODEL_RESULTS = root_path / "backend/model/output" # text files with model prediction data

DIR_IMG_REL = "/static/images/" # food label icons for display on website
DIR_WEB_RESULT_IMG_REL = "/static/input_images/" # model output images with bounding boxes, web-accessible directory

DIR_MODEL_INPUT = root_path / "backend/input_images" # images taken by camera to be fed into model
DIR_WEB_RESULT_IMG = root_path / "gui/static/input_images" # model output images with bounding boxes, web-accessible directory
