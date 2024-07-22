# How to run our model

With the provided `libdarknet.so` file, Darknet should run out of the box via the `darknet.py` python wrapper and you can skip right to step 2.

Note that this only works for Linux-based systems.
If it doesn't work or you are using Windows, Darknet needs to be compiled from scratch.
Below are the respective instructions for the relevant Jetson Nano device.

## 1 - Compiling Darknet on Jetson Nano

Clone the Darknet git repository
`git clone https://github.com/AlexeyAB/darknet`

Open the Makefile and set these variables to 1:
```
GPU=1
CUDNN=1
CUDNN_HALF=1
OPENCV=1
OPENMP=1
LIBSO=1
```

Comment the ARCH block and uncomment the line following: *Jetson TX1, Tegra X1, DRIVE CX, DRIVE PX*
```
ARCH= -gencode arch=compute_53,code=[sm_53,compute_53]
```

Replace NVCC path:
`NVCC=/usr/local/cuda/bin/nvcc`

Compile Darknet:
```
$ cd darknet/
$ make
```

Make sure OpenCV is compiled with GPU and GStreamer support. We already provide such a setup in our Jetson Nano.

Finally, place the `libdarknet.so` file resulting from the compilation into this directory.

## 2 - Testing the model:

Try running the model demo to see if everything works.
A window will open, showing the live camera feed with drawn in bounding boxes for detected food labels.

### Running the demo:

Run our YOLO model in standalone mode with a video stream from the camera:
```
$ cd backend/model/
$ python3 label_detector_demo.py
```
