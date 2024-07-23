import cv2
import backend.model.model_utils as model
from backend.model.model_utils import darknet, network, class_names, class_colors


# Initialize the CSI camera (don't change code)
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=960,
    capture_height=960,
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


def capture_video():
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=4), cv2.CAP_GSTREAMER)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    frame_count = 0
    detections = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 0)
            frame_count += 1
            
            # Feed 1 frame per 10 frames to darknet
            if frame_count % 30 == 0:
                darknet_image = model.convert_to_darknet_image(frame)
                
                # Detection
                detections = darknet.detect_image(network, class_names, darknet_image)
                darknet.free_image(darknet_image)
            
            # Draw bbs
            image = darknet.draw_boxes(detections, frame, class_colors)
            cv2.imshow('Detections', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Error: Could not read frame.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_video()
