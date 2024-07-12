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
                    print("empty dir")
                    yield "data: clear\n\n"
                    break
                else:
                    model_labels_new = util.read_yolo_output(model_output)
                    if model_labels_new != model_labels: # clear labels then return new ones from outer loop
                        model_labels = model_labels_new
                        print("new image")
                        yield "data: clear\n\n"
                        break
                    else:
                        sleep(0.1)
    
    return Response(gen_labels(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, 
            threaded=True)
