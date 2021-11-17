import cv2 as cv


'''
Followed tutorial here: https://www.pyimagesearch.com/2018/08/06/tracking-multiple-objects-with-opencv/
'''


# CSRT for slower FPS and higher object tracking accuracy
# KCF: faster FPS slightly lower object tracking

# Create multi tracker object
trackers = cv.legacy.MultiTracker_create()

# Get video capture
capture = cv.VideoCapture(0)


# Changing resolution to be smaller (both for view and performance of tracking)
def changeRes(width, height):
    capture.set(3,width)
    capture.set(4,height)

changeRes(200, 200)


# Checks if two bounding boxes overlap so it doesn't continually add tracking boxes
def overlaps(box1, box2):
    (x1, y1, w1, h1) = [int(v) for v in box1]
    (x2, y2, w2, h2) = [int(v) for v in box2]

    x = max(x1, x2)
    y = max(y1, y2)
    w = min(x1 + w1, x2 + w2) - x
    h = min(y1 + h1, y2 + h2) - y
    if w < 0 or h < 0:
        return False
    return True



# Main video read loop
count = 0
boxes = None
while True:
    # Reads a frame from the video capture
    isTrue, frame = capture.read()

    # Two options:
    # Use canny edge detection to find robots
    # Train Cascade classifier on images

    # Canny edge detection
    # Grayscale frame
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Blur frame (might not be needed)
    #blur = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
    #cv.imshow("Blur", gray)

    # Cany edges
    cany = cv.Canny(gray, 125, 175) 
    #cv.imshow("Cany", cany)
    # Get edges from cany frame
    contours, _ = cv.findContours(cany, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cont in contours:
        area = cv.contourArea(cont)
        # Only use large objects (needs calibrating)
        if area > 50:
            # Get rectangle around object
            x, y, w, h = cv.boundingRect(cont)
            obj = (x, y, w, h)
            overlap = False
            if boxes is not None:
                for box in boxes:
                    # Check if current box overlaps with another tracking box
                    overlap = overlaps(obj, box)
                    if overlap:
                        break
            if not overlap:
                # Adds tracker for detected object as it doesn't overlap
                print('Adding tracker')
                tracker = cv.legacy.TrackerKCF_create()
                trackers.add(tracker, frame, obj)


    
    # Gets new bounding boxes for objects being tracked
    (success, boxes) = trackers.update(frame)


    # Redisplays boxes
    for box in boxes:
        (x, y, w, h) = [int(v) for v in box]
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Shows frame
    cv.imshow("Video", frame)
    key = cv.waitKey(1) & 0xFF

    # Press 'd' to end video capture
    if key == ord("d"):
        break



capture.release()
cv.destroyAllWindows()


