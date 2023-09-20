import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)
def changeRes(width, height):
    cap.set(3, width)
    cap.set(4, height)
changeRes(100, 100)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    #Capture frame by frame
    ret, frame = cap.read()

    arucoDict = cv.aruco.Dictionary(cv.aruco.DICT_4x4_250)
    arucoParams = cv.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

    #Operations on the frame
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

#After done release capture
cap.release()
cv.destroyAllWindows()
