# AISS_CV_Group_6 - Food Label Recognition

Detect common labels on food products using computer vision and provide information on them.

## Setup Frontend

The frontend is a webapp showing information on detected labels. For this, model output is read from certain folders.

Execute the commands below to start the frontend (open terminal in the /main/ folder):
```
pip install .
streamlit run gui/main.py
```

Press Ctrl+C inside the terminal to stop the frontend.

## Setup Backend

### 1-Compiling darknet on Jetson Nano:
git clone https://github.com/AlexeyAB/darknet (in /main/backend/ folder)

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

Compile darknet:
```
$ cd ~/darknet
$ make
```

Make sure OpenCV is compiled with GPU and GStreamer support. We already provide such a setup in our Jetson Nano.

### 2-Running our model:

#### 2.1-Running the demo:

```
$ cd ~/darknet
$ python3 label_detector_demo_optimized.py
```

#### 2.2-Running the frontend:

```
$ cd ~/darknet
$ python3 server.py
$ cd ~/darknet/static/input_images
$ nvgstcapture-1.0 #press j key
```

## Wiki

Important Information can be found here: https://gitlab.kit.edu/ukona/aiss_cv_group_6/-/wikis

## Labelling

**IMPORTANT**
Please read the [labelling wiki](https://gitlab.kit.edu/ukona/aiss_cv_group_6/-/wikis/Labeling-Convention) before labelling any images to ensure consistency with our labelling rules!
