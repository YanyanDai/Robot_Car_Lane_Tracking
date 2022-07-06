import cv2
frameWidth = 480
frameHeight = 240
camSet = "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"

cap = cv2.VideoCapture(camSet)
#cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,100)
def getImg(display = False, size = [480,240]):
    _, img = cap.read()
    img = cv2.resize(img, (size[0],size[1]))
    if display:
        cv2.imshow('img', img)
        
    return img

if __name__ == '__main__':
    while True:
        img = getImg(True)
        cv2.waitKey(1)