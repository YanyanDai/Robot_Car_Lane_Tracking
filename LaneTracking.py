import cv2
from numpy.lib.shape_base import tile
import LaneDetectionModule as ldm 
import StopPointDetectionModule as spm
import CameraModule as cm
import SerialModule as sm 
import numpy as np 
import time
import utlis

intialTrackBarVals = [35,10,15,107]
utlis.initializeTrackbars(intialTrackBarVals)

ser = sm.initconnection('/dev/ttyACM0', 115200)

def trackLane(curveval,NoLane):
    

def main():
    img = cm.getImg(False,size=[240,120])
    curve= ldm.getLaneCurve(img,display=2)
    NoLane = spm.getStopPoint(img,display=0)
    trackLane(curve,NoLane)
    key = cv2.waitKey(1)
    if key== ord('q'):
        sm.sendData(ser,[0,0],4)

if __name__=='__main__':
    sm.sendData(ser,[0,0],4)
    time.sleep(6)
    while True:
        main()
    
