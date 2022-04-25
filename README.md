## Table of contents
* [Information_Extraction_GCN](#Information_Extraction_GCN)
* [Prerequisites](#prerequisites)
* [Dependencies](#dependencies)
* [Initial_setup](#initial_setup)
* [Python_files_description](#Python_files_description)
* [Usage](#usage)
* [Resources](#resources)

# Information_Extraction_GCN
The task of automatically extracting structured information from unstructured and/or semi-structured machine-readable texts is known as information extraction (IE).

This project contains python scripts to generate training data for Graph convolution networks (GCN). 
The data generated can be used for 6D pose estimation. The FUNSD dataset is used in this . 

## Prerequisites
Follow the following steps before going to next steps
This project is tested and works without errors on mac OS and python 2.7

* install anaconda or miniconda
* set up a virtual environment using "conda env create -n  -f env.yml"
* activate a virtual environment using "conda activate GCN_Info_extraction"

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

## Initial_setup
Print the aruco markers in standard size and paste it on a flat surface in a rectangular format, as showin this image. The aruco markers need 
to be clearly visible. The object of interest need ot be placed firmly inside the boundary

![](images/needle.jpg)

Download the FUNSD dataset from the website(https://guillaumejaume.github.io/FUNSD/)

## Python_files_description
* config.ini 

[input] 

train_data_path = training data path of FUNSD dataset
test_data_path = test data path of FUNSD dataset

[output]

raw_data_path = raw data path of processed for GCN to run raw_data_creation.py
processed_data_path = final pre-processed data to get created after running data_for_GCN.py

* each_sample_folder_creation_with_data.py 

Reads in config file to fetch training dat path. 
Creates a folder named 'each_sample_folder' and also it creates inside a seperate folder for each sample listed in the train_data_path.
It copies both image and annotation for files of respective sample to their respective folder created inside each_sample_folder. 
It runs the pre-processing script 'raw_data_info_extraction_files_creation.py' to generate 'test.txt', 'test_image.txt' and 'test_bbox.txt' files for each sample.

* raw_data_creation.py 

Reads in required path variables from config.ini. 
Creates a folders 'img' and 'box', inside the 'data/raw'.
Copy each sample's image from actual dataset to 'data/raw/img' folder.
Prepares a dataframe with columns 'xmin','ymin','xmax','xmin','word','label' using respective files created while training LayoutLM.
Finally saves each sample's dataframe to 'data/raw/box' folder.

* raw_data_info_extraction_files_creation.py 

It pareses argument --data_dir, which reads in annotation of each sample and generates true values file 'test.txt', words with their actual bounding boxes and image
coordinates 'test_image_.txt' and words with their normalized value bounding boxes 'test_bbox.txt' files. 

* train_data_for_GCN.py 

Returns a one big graph with unconnected graphs of samples present in '/data/raw/box' folder. For every sample in the folder creates a graph by calling 'Grapher' class. 
Assigns number to all the labels available. Batches the list of graphs using 'torch_geometric' library. This batched data is saved as '.dataset' format using torch.

* graph.py 

This file has Grapher class, which is instantiated inside 'train_data_for_GCN.py' to create a big graph with unconnected graphs of samples.
Grapher class is used to generate the graph in a dictionary form and a dataframe with relative distances between nodes. This class is also used to calculate features  

* test_ocr.py 

To create dataframe which is necessary for GCN model, to train by using pytesseract(OCR).

* util.py 

This file consists of function to read string, number and boolean values.

* inference_data_for_GCN.py 

prepares i.e. creates graphs for test data and stores in '/data/test/processed/' folder in '.dataset' format.

* final_model.py 

Loads in the data processed  from the folder '/data/processed' and Parses the command line arguments as training parameters.
It has a class Net which creates 'GCN' model or 'ChebConv' model. These models are further trained with training data and tested with testing data.
Training and testing accuracy is logged for every epoch and trained model is saved to 'data/processed' folder.

* inference.py -

This file reads in test data from 'data/test/processed' and evaluates the model with confusion matrix and F1 score and obtaines the inference.

## Usage
* Step1 

  Folder creation and preprocess respective annotation.
  ```
  python3 pipeline/1_each_sample_folder_creation_with_data.py -c config.ini"
  ```

* Step2 

  Raw data preparation for GCN.
  ```
  "python3 pipeline/3_raw_data_creation.py -c config.ini"
  ```

* Step3 

  Graph creation for training data.
  ```
  "python3 pipeline/5_train_data_for_GCN.py"
  ```

* Step4 

  To define and train GCN model.
  ```
  "python3 models/1_final_model.py --model GCN --epochs 100 --lr 0.001 --verbose 1"
  ```

* Step5 

  To get predicitons on test data using trained model.
  ```
  "python3 models/2_inference.py --model GCN --verbose 1"
  ```

Optional: 

To get bounding box coordinates and words extracted from image using pytesseract.
```
"python3 pipeline/test_ocr.py"
```
 
