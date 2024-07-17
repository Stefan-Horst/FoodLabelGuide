from flask import Flask, Response, json, render_template
from time import sleep
from utils.globals import *
import utils.util as util
import cv2
import darknet
import os

app = Flask(__name__)

label_dict = util.read_label_dict("label_dict.json")

#Loading darknet config and weights
network, class_names, class_colors = darknet.load_network(
    "label_detector/yolov4-tiny-labeldetector.cfg",
    "label_detector/obj.data",
    "label_detector/yolov4-tiny-labeldetector.weights"
)

width = darknet.network_width(network)
height = darknet.network_height(network)

def convert_to_darknet_image(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height), interpolation=cv2.INTER_LINEAR)
    darknet_image = darknet.make_image(width, height, 3)
    darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
    return darknet_image

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/lbl")
def stream_labels():
    def gen_labels():
        yield "data: clear\n\n" # reset at beginning

        model_input_img = util.get_newest_file_in_dir(DIR_INPUT_IMG)
        while model_input_img == "": # wait until file exists in directory
            sleep(0.1)
            model_input_img = util.get_newest_file_in_dir(DIR_INPUT_IMG)
        
        frame = cv2.imread(str(model_input_img))
        darknet_image = convert_to_darknet_image(frame)
        #Detection
        detections = darknet.detect_image(network, class_names, darknet_image)
        darknet.free_image(darknet_image)
        #Draw bbs
        image = darknet.draw_boxes(detections, frame, class_colors)
        cv2.imwrite(os.path.join(os.getcwd(), DIR_MODEL_RESULTS / "result.jpg"), image)

        last_image = model_input_img
        last_data_list = None
        while True:
            model_input_img = util.get_newest_file_in_dir(DIR_INPUT_IMG)
            if model_input_img != last_image:
                print("sa")
                frame = cv2.imread(str(model_input_img))
                darknet_image = convert_to_darknet_image(frame)
                #Detection
                detections = darknet.detect_image(network, class_names, darknet_image)
                darknet.free_image(darknet_image)
                #Draw bbs
                image = darknet.draw_boxes(detections, frame, class_colors)
                cv2.imwrite(os.path.join(os.getcwd(), DIR_MODEL_RESULTS / "result.jpg"), image)
                last_image = model_input_img

            data_list = []
            for label in detections:
                img_path, name, description = util.get_label_data(label[0], label_dict)
                data = {
                    "img_path": str(img_path),
                    "name": name,
                    "description": description
                }
                data_list.append(json.dumps(data))

            if data_list != last_data_list:
                yield "data: clear\n\n"
                for data in data_list:
                    yield f"data: {data}\n\n"
                last_data_list = data_list
            else:
                sleep(0.1)
    
    return Response(gen_labels(), mimetype="text/event-stream")


@app.route("/img")
def stream_images():
    def gen_image_urls():
        yield "data: clear\n\n" # reset at beginning

        model_input_img = util.get_newest_file_in_dir(DIR_INPUT_IMG, full_path=False)
        while model_input_img == "": # wait until file exists in directory
            sleep(0.1)
            model_input_img = util.get_newest_file_in_dir(DIR_INPUT_IMG, full_path=False)
        yield f"data: {DIR_INPUT_IMG_REL + model_input_img}\n\n"

        while True:
            model_input_img_new = util.get_newest_file_in_dir(DIR_INPUT_IMG, full_path=False)
            if model_input_img_new == "": # clear image if directory is cleared
                yield "data: clear\n\n"
            elif model_input_img_new != model_input_img:
                model_input_img = model_input_img_new
                yield f"data: {DIR_INPUT_IMG_REL + model_input_img}\n\n"
            else:
                sleep(0.1)
    
    return Response(gen_image_urls(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, 
            threaded=True)

