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
import revpimodio2


class PosValSlave():
    def __init__(self):

        self.rpi = revpimodio2.RevPiModIO(64, autorefresh=True)

        self.rpi.handlesignalend()

    def main(self):

        circles = Preprocess('img19.jpg','medianBlur3','Hough')
        print("X :",circles[0,0], "Y :",circles[0,1], "Z :", 999)
        x = circles[0,0]
        y = circles[0,1]
        z = 999
        pos = [x,y,z]

        return pos

    def cyclefunction(self, cycletools):

        position = self.main()
        # Setting position X, Y, Z values
        self.rpi.io.PosX.value = position[0]

        self.rpi.io.PosY.value = position[1]

        self.rpi.io.PosZ.value = position[2]

    def start(self):

        self.rpi.cycleloop(self.cyclefunction, cycletime=1000)

if __name__ == "__main__":
    root = PosValSlave()
    root.start()