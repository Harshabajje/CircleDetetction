revpi_selection = 'LH'
# revpi_selection = 'RH'

# !/usr/bin/env python
# sudo chmod +x *.py  # in terminal on RevPI to make the .py executable


# ==========IMPORTS==========================================

import os
# from os import mkdir
from os.path import join, exists
import sys
# from sys import exit
import time
from datetime import datetime
from datetime import date
import cv2 as cv
# from cv2 import resize, cvtColor, COLOR_BAYER_RG2RGB, imwrite, imread, threshold, IMREAD_UNCHANGED, THRESH_BINARY, THRESH_OTSU
from pypylon import pylon
from pypylon import genicam
import json
# from json import load

# ==========END IMPORTS======================================


# ==========FUNCTIONS========================================

def init_cam(cam):
    """
    :param cam: camera specific settings
    :return: camera object
    """
    print(cam[0]['Name'])
    empty_camera_info = ptl.CreateDeviceInfo()
    empty_camera_info.SetPropertyValue('IpAddress', cam[0]['IpAddress'])
    camera_device = factory.CreateDevice(empty_camera_info)
    cam_obj = pylon.InstantCamera(camera_device)
    cam_obj.Open()

    # general settings
    cam_obj.CenterX.Value = centerX
    cam_obj.CenterY.Value = centerY
    cam_obj.Height.Value = height
    cam_obj.Width.Value = width
    cam_obj.GevSCPD.SetValue(inter_packet_delay)
    # cam_obj.GevSCPD.Value = inter_packet_delay
    # cam_obj.GevSCPSPacketSize.SetValue(inter_packet_size)
    # cam_obj.GevSCPSPacketSize.Value = inter_packet_size
    cam_obj.PixelFormat = pixel_format
    cam_obj.MaxNumBuffer = max_num_buffer
    # cam_obj.GammaEnable = gamma_enable

    # specific settings
    # cam_obj.StartGrabbingMax(count_of_images_to_grab)  # wenn dies aktiviert ist, dann ist nach der ersten Aufnahme das Bild weiß
    cam_obj.ExposureTimeRaw.SetValue(cam[0]['ExposureTime'])
    cam_obj.GainRaw.SetValue(cam[0]['Gain'])
    cam_obj.GammaEnable = cam[0]['GammaEnable']

    return cam_obj
# -----------------------------------------------------------

def take_picture(cam_obj, cam):
    """
    :param cam_obj: camera object
    :param cam: camera specific settings
    :return: taken image
    """
    print('Take picture from:', cam[0]['Name'])
    cam_obj.StartGrabbingMax(count_of_images_to_grab)
    while cam_obj.IsGrabbing():
        # grab = cam_obj.RetrieveResult(5000, pylon.TimeoutHandling_Return)  # 5000 anstatt 100
        grab = cam_obj.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grab.GrabSucceeded():
            # print("SizeX: ", grab.Width)
            # print("SizeY: ", grab.Height)
            img = grab.Array
            cam_obj.StopGrabbing()
            grab.Release()
            # break
        else:
            print("Error: ", grab.ErrorCode, grab.ErrorDescription)
        # grab.Release()
    # cam_obj.StopGrabbing()
    # grab.Release()

    img = cv.cvtColor(img, cv.COLOR_BAYER_RG2RGB)

    # Entfernen aller unzulaessigen Zeichen im Dateinamen
    filename = picture_time + '_' + cam[0]['Name']
    filename = filename.replace(':', '-')
    filename = filename.replace(' ', '')
    # TODO: Hier kommt noch der Input von der SPS hin, die zaehlt, das wievielte Teil es ist und der DMC

    # img_to_save = cv.resize(img, (0, 0), fx=0.5, fy=0.5)  # Bild für das Speichern verkleinern, aktuell auf 10% der Groeße
    img_to_save = img
    global bauteilnummer
    cv.imwrite(join(folder_to_safe_images, filename + '_' + str(bauteilnummer) + '.jpg'), img_to_save)

    return img
# -----------------------------------------------------------

def check_folder_structure():
    """
    :return: nothing
    creates the folder structure depending on the actual day and hour
    """
    if not exists(join(filepath, today)):  # check Tagesordner: YYYY-MM-DD
        os.mkdir(join(filepath, today))  # Erstelle Tagesordner
        os.mkdir(join(filepath, today, today + '_' + hour))  # und Stundenordner: YYYY-MM-DD_HH
    else:
        if not exists(join(filepath, today, today + '_' + hour)):  # check Stundenordner YYYY-MM-DD_HH
            os.mkdir(join(filepath, today, today + '_' + hour))  # erstelle Stundenordner
# -----------------------------------------------------------

# ==========END FUNCTIONS====================================


# ==========LOADING CONFIG===================================

read_config = True
print('Read config...')
while read_config:
    try:
        # ----------read config.json-------------------------
        if revpi_selection == 'LH':
            with open("config_LH.json") as jsonFile:
                config = json.load(jsonFile)
                jsonFile.close()
        elif revpi_selection == 'RH':
            with open("config_RH.json") as jsonFile:
                config = json.load(jsonFile)
                jsonFile.close()

        # ----------general camera settings------------------
        centerX = config['GeneralCameraSettings'][0]['centerX']
        centerY = config['GeneralCameraSettings'][0]['centerY']
        width = config['GeneralCameraSettings'][0]['width']
        height = config['GeneralCameraSettings'][0]['height']
        inter_packet_delay = config['GeneralCameraSettings'][0]['InterPacketDelay']
        inter_packet_size = config['GeneralCameraSettings'][0]['InterPacketSize']
        pixel_format = config['GeneralCameraSettings'][0]['PixelFormat']
        # gamma_enable = config['GeneralCameraSettings'][0]['GammaEnable']

        # ----------specific camera settings-----------------
        cam_1 = config['Cams'][0]['Cam1']
        cam_2 = config['Cams'][0]['Cam2']
        cam_3 = config['Cams'][0]['Cam3']
        cam_4 = config['Cams'][0]['Cam4']
        cam_5 = config['Cams'][0]['Cam5']
        cam_6 = config['Cams'][0]['Cam6']
        cam_7 = config['Cams'][0]['Cam7']
        cam_8 = config['Cams'][0]['Cam8']
        cam_9 = config['Cams'][0]['Cam9']
        cam_10 = config['Cams'][0]['Cam10']
        cam_11 = config['Cams'][0]['Cam11']
        cam_12 = config['Cams'][0]['Cam12']
        cam_13 = config['Cams'][0]['Cam13']
        cam_14 = config['Cams'][0]['Cam14']
        # cam_15 = config['Cams'][0]['Cam15']

        # ----------general settings-------------------------
        filepath = config['GeneralSettings'][0]['FilePath']
        count_of_images_to_grab = config['GeneralSettings'][0]['CountOfImagesToGrab']  # maximum number of tries to get pictures
        prob = config['GeneralSettings'][0]['Prob']  # Genauigkeit für die IO-Erkennung. Je höher, desto unwahrscheinlicher ist falsch IO, gleichzeitig steigt aber auch falsch NIO
        max_num_buffer = config['GeneralSettings'][0]['MaxNumBuffer']
        server_host = config['GeneralSettings'][0]['ServerHost']
        server_port = config['GeneralSettings'][0]['ServerPort']

        read_config = False
        print('Config read in.')
    except:
        print('config.json incorrect -> revise')
        input('Press Enter to load again...')

# ==========END LOADING CONFIG===============================


# ==========INIT CAM OBJECTS=================================

factory = pylon.TlFactory.GetInstance()
ptl = factory.CreateTl('BaslerGigE')

init_cam_objects = True
print('Initialize cameras...')
while init_cam_objects:
    try:
        # cam_obj_1 = init_cam(cam_1)
        # cam_obj_2 = init_cam(cam_2)
        # cam_obj_3 = init_cam(cam_3)
        # cam_obj_4 = init_cam(cam_4)
        # cam_obj_5 = init_cam(cam_5)
        # cam_obj_6 = init_cam(cam_6)
        # cam_obj_7 = init_cam(cam_7)
        # cam_obj_8 = init_cam(cam_8)
        # cam_obj_9 = init_cam(cam_9)
        # cam_obj_10 = init_cam(cam_10)
        # cam_obj_11 = init_cam(cam_11)
        # cam_obj_12 = init_cam(cam_12)
        # cam_obj_13 = init_cam(cam_13)
        # cam_obj_14 = init_cam(cam_14)
        # cam_obj_15 = init_cam(cam_15)
        print('Cameras initialized.')

        init_cam_objects = False

    except genicam.GenericException as e:
        print("An exception occurred. ", str(e))  # e.GetDescription())
        # sys.exit()

    except:
        # init_cam_objects = False
        print('Fehler. Falsche Camera IP-Addressen? Camera nicht angeschlossen? . Besseres Fehlermanagement aufbauen!')
        input('Error management still needs to be built up! Press \'Enter\' to continue...')

# ==========END INIT CAM OBJECTS=============================


# ==========MAIN PROGRAM=====================================

while True:
    eingabe = input('Start (y) or cancel (n) measurement: ')  # eingabe = start, wenn es soweit ist
    if eingabe == 'y':
        try:
            bauteilnummer = input('Bauteil-Nr.: ')
            start_time = time.time()
           
            # ----------create timestamps--------------------
            today = date.today()
            today = str(today)

            now = datetime.now().strftime("%H:%M:%S")
            now = str(now)

            hour = datetime.now().strftime('%H')
            hour = str(hour)

            picture_time = today + '_' + now

            # ----------folder structure---------------------
            folder_to_safe_images = join(filepath, today, today + '_' + hour)

            check_folder_structure()  # creates the folder structure if not exist

            # take_picture(cam_obj_1, cam_1)
            # take_picture(cam_obj_2, cam_2)
            # take_picture(cam_obj_3, cam_3)
            # take_picture(cam_obj_4, cam_4)
            # take_picture(cam_obj_5, cam_5)
            # take_picture(cam_obj_6, cam_6)
            # take_picture(cam_obj_7, cam_7)
            # take_picture(cam_obj_8, cam_8)
            # take_picture(cam_obj_9, cam_9)
            # take_picture(cam_obj_10, cam_10)
            # take_picture(cam_obj_11, cam_11)
            # take_picture(cam_obj_12, cam_12)
            # take_picture(cam_obj_13, cam_13)
            # take_picture(cam_obj_14, cam_14)
            # take_picture(cam_obj_15, cam_15)
            
        except genicam.GenericException as e:
            print("An exception occurred.", e.GetDescription())  # str(e))

        # except:
        #     print('Error management still needs to be built up!')
        #     # Errormanagement muss noch sinnvoll aufgebaut werden

    else:
        # ----------close cam objects------------------------
        # cam_obj_1.Close()
        # cam_obj_2.Close()
        # cam_obj_3.Close()
        # cam_obj_4.Close()
        # cam_obj_5.Close()
        # cam_obj_6.Close()
        # cam_obj_7.Close()
        # cam_obj_8.Close()
        # cam_obj_9.Close()
        # cam_obj_10.Close()
        # cam_obj_11.Close()
        # cam_obj_12.Close()
        # cam_obj_13.Close()
        # cam_obj_14.Close()
        # cam_obj_15.Close()
        print('Measurement ended.')
        sys.exit(0)

# ==========END MAIN PROGRAM=================================
