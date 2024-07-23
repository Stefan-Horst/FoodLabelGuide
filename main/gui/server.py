import os
from flask import Flask, Response, json, render_template
from time import sleep
from utils.globals import *
import utils.util as util
import backend.model.model_utils as model


app = Flask(__name__)

label_dict = util.read_label_dict("label_dict.json")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/lbl")
def stream_labels():
    def gen_labels():
        yield "data: clear\n\n" # reset at beginning

        last_model_input_img = ""
        last_data_list = []
        while True:
            model_input_img = util.get_newest_file_in_dir(DIR_MODEL_INPUT)
            # wait until file exists in directory
            while model_input_img == "":
                sleep(0.1)
                model_input_img = util.get_newest_file_in_dir(DIR_MODEL_INPUT)

            # make sure image can actually be loaded (into darknet)
            try:
                detections = model.detect_image(model_input_img)

                # only save image to web folder if it's new
                if model_input_img != last_model_input_img:
                    print("lbl: input ", model_input_img)
                    model.save_current_image()
                    last_model_input_img = model_input_img
            except:
                detections = []
                print("lbl: file removed / error during detection")
                continue

            if len(detections) > 0:
                data_list = []
                # generate label info for each detection
                for label in detections:
                    img_path, name, description = util.get_label_data(label[0], label_dict)
                    data = {
                        "img_path": str(img_path),
                        "name": name,
                        "description": description
                    }
                    data_list.append(data)
                # keep each detected label only once for label list (labels can be detected multiple times per image)
                data_list = util.get_uniques(data_list, key=lambda x: x["name"])
                # make sure list containing the same labels is also always in same order
                data_list.sort(key=lambda x: x["name"])
                

                # only update label info if labels have changed
                if data_list != last_data_list:
                    yield "data: clear\n\n"
                    for data in data_list:
                        print(f"lbl: {data['name']}, {data['img_path']}")
                        yield f"data: {json.dumps(data)}\n\n"
                    last_data_list = data_list
                    continue
            else:
                # clear label info if no labels are detected and it hasn't been cleared yet
                if last_data_list != []:
                    print("lbl: no label detections")
                    yield "data: clear\n\n"
                    last_data_list = []

            sleep(0.1)
    
    return Response(gen_labels(), mimetype="text/event-stream")


@app.route("/img")
def stream_images():
    def gen_image_urls():
        yield "data: clear\n\n" # reset at beginning

        last_model_input_img = ""
        while True:
            model_input_img = util.get_newest_file_in_dir(DIR_WEB_RESULT_IMG, full_path=False)

            # clear image if directory is cleared
            if model_input_img == "" and last_model_input_img != "":
                print("img: empty dir")
                yield "data: clear\n\n"
                last_model_input_img = ""
                continue
            # only update image if image has changed
            elif model_input_img != last_model_input_img:
                print("img: ", DIR_WEB_RESULT_IMG_REL + model_input_img)
                yield f"data: {DIR_WEB_RESULT_IMG_REL + model_input_img}\n\n"
                last_model_input_img = model_input_img
                continue

            sleep(0.1)
    
    return Response(gen_image_urls(), mimetype="text/event-stream")


if __name__ == "__main__":
    # clear image directories to start with fresh blank web page
    try: 
        for f in os.listdir(DIR_MODEL_INPUT):
            os.remove(DIR_MODEL_INPUT / f)
        print("startup: dir cleared: ", str(DIR_MODEL_INPUT))

        for f in os.listdir(DIR_WEB_RESULT_IMG):
            os.remove(DIR_WEB_RESULT_IMG / f)
        print("startup: dir cleared: ", str(DIR_WEB_RESULT_IMG))
    except:
        print("startup: could not clear image directories")

    # start flask server
    app.run(host="0.0.0.0", # -> server visible in network, not just host computer
            debug=True, 
            threaded=True)

