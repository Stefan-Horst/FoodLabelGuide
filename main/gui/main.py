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
        
        while True: # make sure image can actually be loaded
            try:
                model_labels = util.read_yolo_output(model_output)
                break
            except:
                print("lbl: file removed")

            while model_output == "": # wait until file exists in directory
                sleep(0.1)
                model_output = util.get_newest_file_in_dir(DIR_MODEL_RESULTS)

        while True:
            for label in model_labels.keys():
                img_path, name, description = util.get_label_data(label, label_dict)
                data = {
                    "img_path": str(img_path),
                    "name": name,
                    "description": description
                }
                print("lbl: ", json.dumps(data))
                yield f"data: {json.dumps(data)}\n\n"

            while True:
                model_output_new = util.get_newest_file_in_dir(DIR_MODEL_RESULTS)
                if model_output_new == "" and model_output != "": # clear labels if directory is cleared
                    model_output = ""
                    model_labels = ""
                    print("lbl: empty dir")
                    yield "data: clear\n\n"
                elif model_output_new != "":
                    model_output = model_output_new
                    try: # make sure image can actually be loaded
                        model_labels_new = util.read_yolo_output(model_output)
                    except:
                        print("lbl: file removed")
                        sleep(0.1)
                        continue

                    if model_labels_new != model_labels: # clear labels then return new ones from outer loop
                        model_labels = model_labels_new
                        print("lbl: new image")
                        yield "data: clear\n\n"
                        break
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
        print("img: ", DIR_INPUT_IMG_REL + model_input_img)
        yield f"data: {DIR_INPUT_IMG_REL + model_input_img}\n\n"

        while True:
            model_input_img_new = util.get_newest_file_in_dir(DIR_INPUT_IMG, full_path=False)
            if model_input_img_new == "" and model_input_img != "": # clear image if directory is cleared
                model_input_img = ""
                print("img: empty dir")
                yield "data: clear\n\n"
            elif model_input_img_new != model_input_img:
                model_input_img = model_input_img_new
                print("img: ", DIR_INPUT_IMG_REL + model_input_img)
                yield f"data: {DIR_INPUT_IMG_REL + model_input_img}\n\n"
            else:
                sleep(0.1)
    
    return Response(gen_image_urls(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, 
            threaded=True)
