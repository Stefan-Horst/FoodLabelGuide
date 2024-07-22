import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.globals import *

# These paths need to be adjusted to the correct directories
PATH_TO_CONFIG = DIR_MODEL / "cfg/yolov4-tiny-custom-test.cfg"
PATH_TO_WEIGHTS = DIR_MODEL / "data/datasets/backup/yolov4-tiny-custom-test_best.weights"
PATH_TO_WATCH = DIR_MODEL_INPUT


class ImageHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_created(self, event):
        if not event.is_directory:
            if event.src_path.endswith("jpg"):
                self._process_new_image(event.src_path)

    def _process_new_image(self, image_path):
        print(f"Processing new image: {image_path}")
        try:
            EVAL_COMMAND = f"./darknet detector test {PATH_TO_CONFIG} {PATH_TO_WEIGHTS} {image_path}"
            subprocess.run(EVAL_COMMAND, shell=True)

        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e}")


if __name__ == "__main__":
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, PATH_TO_WATCH, recursive=False)
    observer.start()
    print(f"Listening to folder {PATH_TO_WATCH}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
