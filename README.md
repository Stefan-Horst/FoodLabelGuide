# AISS CV Group 6 - Food Label Recognition

**Detect common labels on food products using computer vision and provide information on them.**

The frontend is a webapp showing information on detected labels. The web server uses the Flask framework. The website is built with HTML, CSS, and vanilla JavaScript.

The backend is a YOLOv4-tiny object detection model loaded into the Darknet framework. It is accessed using a python wrapper.

## Setup

The final runnable program is located in the `main` folder. The instructions are based on it as the starting directory.
All code is expected to be run on the Jetson Nano device.

1. Install all packages specified in the `requirements.txt` file
2. Run `sudo python3 setup.py install` to install our custom modules
3. Try starting the demo as specified below. If there is an error with the model, you most likely need to compile Darknet from scratch to make the model work. Please refer to the detailed instructions [here](main/backend/model/README.md).

## Starting the program

### Running the demo:

Run our YOLO model in standalone mode with a video stream from the camera:
```
$ cd backend/model/
$ python3 label_detector_demo.py
```
Press `Q` to stop the demo.

### Running the web app:

Run the web server and the camera in two different terminal windows.

#### Start the web server:
```
$ cd gui/
$ python3 server.py
```
Press `Ctrl+C` inside the terminal window to stop the frontend.

#### Start the camera:
```
$ cd backend/input_images/
$ nvgstcapture-1.0  # Press J+Enter keys to take a picture
```
You can take a picture by entering `J` into the terminal.

Press `Ctrl+C` or enter `Q` to stop the camera.

## Wiki

Important Information can be found in our [Wiki](https://gitlab.kit.edu/ukona/aiss_cv_group_6/-/wikis/pages).

### Labelling:

**IMPORTANT**
Please read the [labelling wiki](https://gitlab.kit.edu/ukona/aiss_cv_group_6/-/wikis/Labeling-Convention) before labelling any images to ensure consistency with our labelling rules!
