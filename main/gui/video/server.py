import cv2
from flask import Flask, Response, json, render_template
from time import sleep
from utils.globals import *
import utils.util as util
import backend.model.model_utils as model


app = Flask(__name__)

label_dict = util.read_label_dict("label_dict.json")

camera = None
detections = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/lbl")
def stream_labels():
    def gen_labels():
        yield "data: clear\n\n"

        global detections
        last_data_list = []
        while True:
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

                # cannot compare detections directly, because they contain ever-changing bbox pos / confidence values
                if data_list != last_data_list:
                    yield "data: clear\n\n"
                    for data in data_list:
                        print(f"lbl: {data['name']}, {data['img_path']}")
                        yield f"data: {json.dumps(data)}\n\n"
                    last_data_list = data_list
            elif detections == [] and last_data_list != []:
                last_data_list = []
                print("lbl: clear labels")
                yield "data: clear\n\n"

            sleep(0.2)

    return Response(gen_labels(), mimetype="text/event-stream")


@app.route("/vid")
def vid():
    def gen_frames():
        frame_count = 0
        global detections
        while True:
            ret, image = camera.read()
            if ret:
                image = cv2.flip(image, 0)

                # predict labels for input image every few frames to reduce resource use
                if frame_count >= 10:
                    try:
                        detections = model.detect_image(image, type="file")
                        image = model.current_image
                        frame_count = 0
                    except:
                        detections = []
                        print("vid: detection error")
                        continue
                else:
                    # all other image should have same dimensions as predicted ones
                    image = model.preprocess_image(image)
                
                if len(detections) > 0:
                    image = model.draw_bounding_boxes(detections, image)

                image = cv2.imencode('.jpg', image)[1].tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

                frame_count += 1
                # theoretically this results in output with ~30 fps
                sleep(0.03)
            else:
                print("vid: could not retrieve camera frame")
    
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# define params for accessing csi camera
def gstreamer_pipeline(
        sensor_id=0,
        capture_width=1640,
        capture_height=1232,
        framerate=30,
        flip_method=4,
    ):
        return (
            "nvarguscamerasrc sensor-id=%d ! video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! video/x-raw, format=(string)BGR ! appsink"
            % (
                sensor_id,
                capture_width,
                capture_height,
                framerate,
                flip_method,
                capture_width,
                capture_height,
            )
        )


if __name__ == "__main__":
    # start recording with csi camera
    camera = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if not camera.isOpened():
        print("startup: camera could not start")

    # start flask server
    app.run(host="0.0.0.0", # -> server visible in network, not just host computer
            #debug=True, 
            threaded=True)
