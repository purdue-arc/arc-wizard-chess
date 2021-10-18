import argparse

import cv2 as cv
from apriltag import apriltag

capture = cv.VideoCapture(0)

def changeRes(width, height):
    capture.set(3,width)
    capture.set(4,height)

changeRes(100, 100)

while True:
    isTrue, frame = capture.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    detector = apriltag("tag36h11")
    results = detector.detect(gray)
    #options = apriltag.DetectorOptions(families="tag36h11")
    #detector = apriltag.Detector(options)
    #results = detector.detect(gray)


    for r in results:
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))

        cv.line(frame, ptA, ptB, (0,255,0),2)
        cv.line(frame, ptB, ptC, (0,255,0),2)
        cv.line(frame, ptC, ptD, (0,255,0),2)
        cv.line(frame, ptD, ptA, (0,255,0),2)

        tagFamily = r.tag_family.decode("utf-8")
        cv.putText(frame, tagFamily, (ptA[0], ptA[1] - 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    cv.imshow('Video', frame)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()
