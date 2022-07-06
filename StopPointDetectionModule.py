import cv2
import numpy as np
from numpy.core.fromnumeric import cumprod
import utlis
import SerialModule as sm 
import time

curveList = []
avgVal = 10
#intialTrackBarVals = [144,160,19,214]
intialTrackBarVals = [70,38,30,214]
utlis.initializeTrackbars(intialTrackBarVals)

ser = sm.initconnection('/dev/ttyACM0', 115200)

def getStopPoint(img, display = 2):

    imgCopy = img.copy()
    imgResult = img.copy()
    ####step 1 image thresholding
    imgThres = utlis.thresholding_Stop(img)
    ####step 2 image wraping
    hT, wT, c = img.shape
    points = utlis.valTrackbars()
    imgWarp  = utlis.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utlis.drawPoints(imgCopy,points)

    ###step3 pixel summation
    #middlepoint, NoLane1, imgHist1 = utlis.getHistogram(imgWarp,minPer=0.5,display=True,region=4) #1/4 figure
    NoLane, imgHist = utlis.getHistogramStop(imgWarp, display=True,region=1)   #1/2 figure
    

    #### Step 4 Display

    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)

    
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3)
        if display == 2:
            imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                                [imgHist, imgLaneColor, imgResult]))
            cv2.imshow('ImageStack', imgStacked)
        elif display == 1:
            cv2.imshow('Resutlt', imgResult)

    return NoLane


if __name__=='__main__':
    #cap = cv2.VideoCapture('vid1.mp4')

    frameWidth = 480
    frameHeight = 240
    camSet = "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
    cap = cv2.VideoCapture(camSet)
    #cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)

    while True:
        _, img = cap.read()
        img = cv2.resize(img,(480,240))   
        NoLane = getStopPoint(img,display=2)
        print('NoLane',NoLane)
        #cv2.imshow('Vid',img)
        cv2.waitKey(1)