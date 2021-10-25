import apriltag
import cv2 as cv

'''
Followed tutorial here: https://www.pyimagesearch.com/2020/11/02/apriltag-with-python/

'''

# Get video capture
capture = cv.VideoCapture(0)


# Change resolution for viewing
def changeRes(width, height):
    capture.set(3,width)
    capture.set(4,height)

changeRes(100, 100)

# Main video loop
while True:
    # Read frame
    isTrue, frame = capture.read()

    # Get grayscale of frame
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Set up apriltag detector to search for apriltags on grayscale image
    options = apriltag.DetectorOptions(families="tag36h11")
    detector = apriltag.Detector(options)
    results = detector.detect(gray)


    # Outlines detected apriltag. Is not a rectangle as this perfectly outlines it
    # regardless of angle of viewing.
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

        # Prints tagFamily (currently tag36h11)
        tagFamily = r.tag_family.decode("utf-8")
        cv.putText(frame, tagFamily, (ptA[0], ptA[1] - 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    # Shows video frame
    cv.imshow('Video', frame)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()
