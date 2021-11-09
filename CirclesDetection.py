#Usage "python CirclesDetection.py --filter filter2D --image H:/TopSurfaceDetection/filterSize3.png"
#param1 = 200,param2 = 25,minRadius = 45 / 65 ,maxRadius = 80/120

from numpy.core.fromnumeric import ndim
from scipy.ndimage import interpolation
import cv2
import imutils
import numpy as np
import argparse
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage.morphology import watershed


print("Here different filters are applied over the 2D images for circle detection")
ap  = argparse.ArgumentParser()
ap.add_argument("--filter", required = True,help="sharpen1,sharpen2,filter2D,medianBlur3,medianBlur5,pyramidMeanShifter,findContourSegmentation,waterShed")
ap.add_argument("--image", required=True, help="Image path")
ap.add_argument("--detection", required=True, help="Hough,findContour,waterShed")
#args = vars(ap.parse_args())
args = ap.parse_args()

def HoughCirclesDetection(origImg,filtImg):
    rows = origImg.shape[0]
    circles = cv2.HoughCircles(filtImg,
                                cv2.HOUGH_GRADIENT,
                                dp = 1.1,
                                minDist = rows/10,
                                param1 = 200,
                                param2 = 25,
                                minRadius = 65,
                                maxRadius = 120)
    outImg = origImg.copy()
    #print(circles[0,:,:])
    print("Number of circles detected : ", circles[0].shape[0])
    circles = np.round(circles[0, :]).astype("int")
    for (x,y,r) in circles:
        #print("X",x,"Y",y,"R",r)
        x = int(x*0.6) 
        y = int(y*0.6)
        r = int(r*0.6)
        cv2.circle(outImg, (x, y), r, (0, 255, 0), 4)
        #print(origImg.shape)
        width = int(origImg.shape[1] * 0.6)
        height = int(origImg.shape[0] * 0.6)
        dim = (width,height)
        #print(dim)
        cv2.putText(outImg, "#{}".format(1 + 1), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        #cv2.namedWindow('output image', cv2.WINDOW_NORMAL)
        outImg = cv2.resize(outImg, dim , interpolation = cv2.INTER_AREA)
        #cv2.imshow("output image",np.hstack([outImg]))
        cv2.imwrite("output120.png", outImg)

def findContour(origImg, filtImg):
    counts = cv2.findContours(filtImg.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    counts = imutils.grab_contours(counts)
    print("The total number of contours identified : ", len(counts))

    for (i,c) in enumerate(counts):
        ((x,y),_) = cv2.minEnclosingCircle(c)
        cv2.putText(origImg, "#{}".format(i + 1), (int(x) - 10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.drawContours(origImg, [c], -1, (0, 255, 0), 2)
    #cv2.imshow("output image",origImg)
    cv2.imwrite("Top1.png", origImg)

def waterShed(origImg, filtImg):
    
    D = ndimage.distance_transform_edt(filtImg)
    localMax = peak_local_max(D, indices= False, min_distance=20, labels= filtImg)

    markers = ndimage.label(localMax, structure= np.ones((3,3)))[0]
    labels = watershed(-D, markers, mask = filtImg)

    print("Total unique segments detected :", len(np.unique(labels))-1)

    for label in np.unique(labels):
        if label == 0:
            continue

        mask =np.zeros(origImg.shape, dtype="uint8")
        mask[labels == label] = 255

        counts = cv2.findContours(filtImg.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        counts = imutils.grab_contours(counts)
        c = max(counts, key = cv2.contourArea)

        ((x,y),r) = cv2.minEnclosingCircle(c)
        cv2.circle(origImg, (int(x), int(y)), int(r), (0, 255, 0), 2)
        cv2.putText(origImg, "#{}".format(label), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.imshow("Output image", origImg)


def Preprocess():
    
    if args.filter == "filter2D" and args.detection == "Hough":
        image = cv2.imread(args.image)
        outImg = image.copy()
        rows = image.shape[0]
        blur_hor = cv2.filter2D(image[:, :, 0], cv2.CV_32F, kernel=np.ones((11,1,1), np.float32)/11.0, borderType=cv2.BORDER_CONSTANT)
        blur_vert = cv2.filter2D(image[:, :, 0], cv2.CV_32F, kernel=np.ones((1,11,1), np.float32)/11.0, borderType=cv2.BORDER_CONSTANT)
        output = ((image[:,:,0]>blur_hor*1.2) | (image[:,:,0]>blur_vert*1.2)).astype(np.uint8)*255
        #cv2.imshow("image",output)

        HoughCirclesDetection(outImg, output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(args.filter, "done")

    elif(args.filter == "medianBlur3" and args.detection == "Hough"):
        image = cv2.imread(args.image)
        outImg = image.copy()
        rows = image.shape[0]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray,3)
        #cv2.imshow("gray", gray)

        HoughCirclesDetection(outImg,gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(args.filter, "done")
    
    elif(args.filter == "medianBlur5" and args.detection == "Hough"):
        image = cv2.imread(args.image)
        outImg = image.copy()
        rows = image.shape[0]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray,5)
        #cv2.imshow("gray", gray)

        HoughCirclesDetection(outImg,gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(args.filter, "done")

    elif(args.filter == "sharpen1" and args.detection == "Hough"):
        image = cv2.imread(args.image)
        outImg = image.copy()
        rows = image.shape[0]
        kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
        image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray,5)

        HoughCirclesDetection(outImg,gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(args.filter, "done")

    

    elif(args.filter == "pyramidMeanShifter" and args.detection == "findContourSegmentation"):
        image = cv2.imread(args.image)
        outImg = image.copy()
        rows = image.shape[0]
        filterImg = cv2.pyrMeanShiftFiltering(image,21,51)
        gray = cv2.cvtColor(filterImg,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        findContour(outImg,thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(args.filter,"done")

    elif(args.filter == "pyramidMeanShifter" and args.detection == "waterShed"):
        image = cv2.imread(args.image)
        outImg = image.copy()
        rows = image.shape[0]
        filterImg = cv2.pyrMeanShiftFiltering(image,21,51)
        gray = cv2.cvtColor(filterImg,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        waterShed(outImg,thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(args.filter,"done")


    else:
        print("please enter the proper inputs")


if  __name__ == "__main__":
    Preprocess()