from numpy.core.fromnumeric import ndim
from scipy.ndimage import interpolation
import cv2
from cv2 import imread,imshow,HOUGH_GRADIENT,HoughCircles   #### import only required functions
import imutils
import numpy as np
import argparse
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage.morphology import watershed

def HoughCirclesDetection(rows, image):
    rows = rows
    ### Rows is constant 
    circles = HoughCircles(image,
                                HOUGH_GRADIENT,
                                dp = 1.0,
                                minDist = rows/10,
                                param1 = 200,
                                param2 = 25,
                                minRadius = 85,
                                maxRadius = 100)

    #print(circles[0,:,:])
    print("Number of circles detected before rules applied : ", circles[0].shape[0])
    
    # Rule 1 : Any radius less than (mean - 2)
    
    circles = np.round(circles[0, :]).astype("int")
    circles = circles[circles[:,2]>(circles[:,2].mean()-2)]
    print("Number of circles detected after applying min radius rule  : ", circles.shape[0])

    # The positions are sorted such that it picks the part always from first row and first
    circles = circles[circles[:, 1].argsort()][:8,:]
    circles = circles[circles[:, 0].argsort()]

    return circles



def Preprocess(image_path,filter,detection):
    
    if filter == "filter2D" and detection == "Hough":
        image = cv2.imread(image_path)
        rows = image.shape[0]
        blur_hor = cv2.filter2D(image[:, :, 0], cv2.CV_32F, kernel=np.ones((11,1,1), np.float32)/11.0, borderType=cv2.BORDER_CONSTANT)
        blur_vert = cv2.filter2D(image[:, :, 0], cv2.CV_32F, kernel=np.ones((1,11,1), np.float32)/11.0, borderType=cv2.BORDER_CONSTANT)
        image = ((image[:,:,0]>blur_hor*1.2) | (image[:,:,0]>blur_vert*1.2)).astype(np.uint8)*255

        circles = HoughCirclesDetection(rows,image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(filter, "done")
        return circles

    elif(filter == "medianBlur3" and detection == "Hough"):
        image = cv2.imread(image_path)
        rows = image.shape[0]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.medianBlur(image,3)

        circles = HoughCirclesDetection(rows,image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(filter, "done")
        return circles
    
    elif(filter == "medianBlur5" and detection == "Hough"):
        image = cv2.imread(image_path)
        rows = image.shape[0]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.medianBlur(image,5)

        circles = HoughCirclesDetection(rows,image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(filter, "done")
        return circles

    else:
        print("please enter the proper inputs")



