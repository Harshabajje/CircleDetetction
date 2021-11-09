#!/usr/bin/python
import os
import sys
import cv2
import json
import util
import time
import imutils
from Circles import *
import argparse
import subprocess
import configparser
import numpy as np

def main():
    # set up a parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=False, default="config.ini", help="Config file")

    # parse arguments
    args = parser.parse_args()
    cfg = args.config
    cfgparser = configparser.ConfigParser()
    res = cfgparser.read(cfg)
    if len(res) == 0:
        print("Error: None of the config files could be read")
        sys.exit(1)

    # read config 
    z_coordinate = util.read_cfg_float (cfgparser,'input','Z_coordinate', default = None)
    image_save_path = util.read_cfg_string(cfgparser,'output','image_save_folder', default= None)
    Filter = util.read_cfg_string(cfgparser,'input','filter',default= None)
    Image_path = util.read_cfg_string(cfgparser,'input','image', default=None)
    Detection = util.read_cfg_string(cfgparser,'input','detection',default=None)

    circles = Preprocess(Image_path,Filter,Detection)
    print("X :",circles[0,0], "Y :",circles[0,1], "Z :", z_coordinate)

if __name__=="__main__":
    start_time = time.time()
    main()
    print("Time taken" ,(time.time() - start_time))