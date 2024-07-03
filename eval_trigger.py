import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PATH_TO_CONFIG = "cfg/yolov4-tiny-custom-test.cfg"
PATH_TO_WEIGHTS = "/home/oguyig00/aiss/aiss_cv_group_6/data/datasets/backup/yolov4-tiny-custom-test_best.weights"


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
    path_to_watch = "./test_dir"  # TODO: Path to images dir needs to be changed
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()
    print(f"Listening to folder {path_to_watch}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
