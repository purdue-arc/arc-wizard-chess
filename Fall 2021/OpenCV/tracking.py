import cv2 as cv
#from tracker import *

capture = cv.VideoCapture(0)

#tracker = EuclideanDistTraker()

def changeRes(width, height):
    capture.set(3,width)
    capture.set(4,height)

#changeRes(100, 100)

object_detector = cv.createBackgroundSubtractorMOG2()

while True:
    isTrue, frame = capture.read()


    #mask = object_detector.apply(frame)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #blur = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
    cany = cv.Canny(gray, 125, 175)



    cv.imshow('Frame', cany)

    #_, mask = cv.threshold(cany, 254, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(cany, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv.contourArea(cnt)
        if area > 50:
            cv.drawContours(frame, [cnt], -1, (0,255,0),2)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),3)

        


    cv.imshow('Video', frame)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()