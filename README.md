## Table of contents
* [Information_Extraction_GCN](#Information_Extraction_GCN)
* [Prerequisites](#prerequisites)
* [Dependencies](#dependencies)
* [Initial_setup](#initial_setup)
* [Usage](#usage)
* [Resources](#resources)

# Information_Extraction_GCN

This project contains python scripts to generate a 3D reconstructed object, RGB,RGBD, color aligned depth images, Bounding boxes. 
The data generated can be used for 6D pose estimation. The video sequence is captured using RealSense depth camera D415. The basic idea
behind is to use aruco markers and ICP algorithm for registration.

For further preprocessing, we might need to use [MeshLab](https://www.meshlab.net/) , [blender](https://www.blender.org/).

## Prerequisites
Follow the following steps before going to next steps
This project is tested and works without errors on mac OS and python 2.7

* install anaconda or miniconda
* set up a virtual environment using "conda env create -n  -f env.yml"
* activate a virtual environment using "conda activate grpcDemo"

## Dependencies
This project requires
* numpy
* pandas
* matplotlib
* torch
* networkx
* sklearn
* pytesseract
* cv2
* torch_geometric

Since we are using Relasense Camera, we need to install the dpendent [libraries](https://github.com/IntelRealSense/librealsense)
```
pip install pyrealsense2
  ```
## Initial_setup
Print the aruco markers in standard size and paste it on a flat surface in a rectangular format, as showin this image. The aruco markers need 
to be clearly visible. The object of interest need ot be placed firmly inside the boundary

![](images/needle.jpg)

## Usage
* Recording
 
  The record script is used to recoed object video sequence uing pyrealsense camera. By default the script records for 40 sconds, which can be changed 
  by adjusting the paramter in the script. we can interupt the recording inbetween by pressing 'q'.
  ```
  python record.py DATASET/Needle
  ```
  While recording please move the camera slowly around the object and make sure atleast 3 aruco markers are clearly visible in the frame. Have proper
  visible light conditions while rcording. Once recording is done, the camera intrinsics are stored in JSON file.

* Computing ground truth poses

  The transformation matrices are calculated between current and first frames using ICP algorithms. and saves it as transforms.npy
  ```
  python gt_poses.py DATASET/Needle
  ```
* Registration

  This script will make use of aruco markers and KNN algorith to identify the edges and corners to find the relation between the frames and 
  finds the transformation matrices, which tells the roation and trnaslation between the frames. This contains some level of noise.
  ```
  python register_scene.py DATASET/Needle
  ```
  The mesh generated contains some noise, the noise level depends on so many factors like light conditions, size of the object of interest and camera
  parameters. We can make use of softwares like meshlab, blender to further preprocess the mesh. Meshlab provides many filters which can automatically 
  detect the noise to certain level. The better the mesh quality, better for the 6D pose estimation
 
* Labels creation

  This creates a mesh, whose AABB is centred to origin. It also produces mask and transformation matrix with respect to new mesh. It also provides us the ground truth 3D           bounding bos values, which later can be used to evaluate the quality of 6D pose matrix.
  ```
  python create_label_files.py DATASET/Needle
  ```
 * Bounding boxes
 
   This creates the annotations file which contains the bounding box values.
   ```
   python get_boundingBox.py
    ```
 
