import cv2
import numpy as np
from numpy.core.fromnumeric import cumprod
import utlis
import SerialModule as sm 
import time

curveList = []
avgVal = 10
#intialTrackBarVals = [144,160,19,214]
#intialTrackBarVals = [70,8,30,214]
intialTrackBarVals = [35,4,15,107]
utlis.initializeTrackbars(intialTrackBarVals)

ser = sm.initconnection('/dev/ttyACM0', 115200)

def getLaneCurve(img, display = 2):

    imgCopy = img.copy()
    imgResult = img.copy()
    ####step 1 image thresholding

    ####step 2 image wraping
   

    ###step3 pixel summation
   

    ####Step 4 Averaging curve value
    

    #### Constraining curve value
    #curve = curve / 100
    

    #### Step 5 Display
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        if display == 2:
            imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                                [imgHist1, imgLaneColor, imgResult]))
            cv2.imshow('ImageStack', imgStacked)
        elif display == 1:
            cv2.imshow('Resutlt', imgResult)
    return curve


if __name__=='__main__':
    #cap = cv2.VideoCapture('vid1.mp4')

    frameWidth = 240#480
    frameHeight = 120#240
    camSet = "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
    cap = cv2.VideoCapture(camSet)
    #cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)

    while True:
        _, img = cap.read()
        img = cv2.resize(img,(frameWidth,frameHeight))
        #getLaneCurve(img)
        start_time = time.time()
        curve= getLaneCurve(img,display=2)
        dur_time = time.time()-start_time
        print('duration time', dur_time)
        #print('curve',curve)
        #cv2.imshow('Vid',img)
        cv2.waitKey(1)
