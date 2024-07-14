from flask import Flask, Response, json, render_template
from time import sleep
from utils.globals import *
import utils.util as util

app = Flask(__name__)

label_dict = util.read_label_dict("label_dict.json")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/lbl")
def stream_labels():
    def gen_labels():
        yield "data: clear\n\n" # reset at beginning

        model_output = util.get_newest_file_in_dir(DIR_MODEL_RESULTS)
        while model_output == "": # wait until file exists in directory
            sleep(0.1)
            model_output = util.get_newest_file_in_dir(DIR_MODEL_RESULTS)
        model_labels = util.read_yolo_output(model_output)

        while True:
            for label in model_labels.keys():
                img_path, name, description = util.get_label_data(label, label_dict)
                data = {
                    "img_path": str(img_path),
                    "name": name,
                    "description": description
                }
                print(json.dumps(data))
                yield f"data: {json.dumps(data)}\n\n"

            while True:
                model_output = util.get_newest_file_in_dir(DIR_MODEL_RESULTS)
                if model_output == "": # clear labels if directory is cleared
                    print("lbl: empty dir")
                    yield "data: clear\n\n"
                    break
                else:
                    model_labels_new = util.read_yolo_output(model_output)
                    if model_labels_new != model_labels: # clear labels then return new ones from outer loop
                        model_labels = model_labels_new
                        print("lbl: new image")
                        yield "data: clear\n\n"
                        break
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
        print(DIR_INPUT_IMG_REL + model_input_img)
        yield f"data: {DIR_INPUT_IMG_REL + model_input_img}\n\n"

        while True:
            model_input_img_new = util.get_newest_file_in_dir(DIR_INPUT_IMG, full_path=False)
            if model_input_img_new == "": # clear image if directory is cleared
                print("img: empty dir")
                yield "data: clear\n\n"
            elif model_input_img_new != model_input_img:
                model_input_img = model_input_img_new
                print(DIR_INPUT_IMG_REL + model_input_img)
                yield f"data: {DIR_INPUT_IMG_REL + model_input_img}\n\n"
            else:
                sleep(0.1)
    
    return Response(gen_image_urls(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, 
            threaded=True)
