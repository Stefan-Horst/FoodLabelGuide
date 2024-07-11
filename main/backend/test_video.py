import cv2
import darknet
import numpy as np


# Initialize the CSI camera (don't change code)
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=416,
    capture_height=416,
    framerate=30,
    flip_method=0,
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

# Loading darknet config and weights
network, class_names, class_colors = darknet.load_network(
    "cfg/yolov4-tiny.cfg",
    "cfg/coco.data",
    "yolov4-tiny.weights"
)

width = darknet.network_width(network)
height = darknet.network_height(network)


def convert_to_darknet_image(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height), interpolation=cv2.INTER_LINEAR)
    darknet_image = darknet.make_image(width, height, 3)
    darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
    return darknet_image


def capture_video():
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 0)
            darknet_image = convert_to_darknet_image(frame)
            
            # Detection
            detections = darknet.detect_image(network, class_names, darknet_image)
            darknet.free_image(darknet_image)
            
            # Draw bbs
            image = darknet.draw_boxes(detections, frame, class_colors)
            cv2.imshow('Detections', image) # comment this out for frontend

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error: Could not read frame.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_video()
