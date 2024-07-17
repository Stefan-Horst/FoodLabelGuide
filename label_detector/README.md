# How to run our model:

## 1-Compiling darknet on Jetson Nano:
git clone https://github.com/AlexeyAB/darknet

Set these variable to 1:
GPU=1
CUDNN=1
CUDNN_HALF=1
OPENCV=1
OPENMP=1
LIBSO=1

Comment the ARCH block and uncomment the following line

For Jetson TX1, Tegra X1, DRIVE CX, DRIVE PX - uncomment:
ARCH= -gencode arch=compute_53,code=[sm_53,compute_53]

Replace NVCC path
NVCC=/usr/local/cuda/bin/nvcc

Compile darknet:
$ cd ~/darknet
# compile
$ make

Make sure OpenCV is compiled with GPU and GStreamer support. We already provide such a setup in our Jetson Nano.

## 2-Running our model:

### 2.1-Running the demo:

$ cd ~/darknet
$ python3 label_detector_demo_optimized.py

### 2.2-Running the frontend:
$ cd ~/darknet
$ python3 server.py
$ cd ~/darknet/static/input_images
$ nvgstcapture-1.0 #press j key
