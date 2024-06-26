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
DIR_IMG = root_path / "gui/resources/images"
DIR_OUTPUT = root_path / "model_output"
DIR_UTIL = root_path / "util"
