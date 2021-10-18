import numpy as np
import cv2 as cv

#import glob
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

#images = glob.glob('*.png')
images = ["starry_night.png"]
while True:
    success, img = cap.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (7, 7), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (7,7), corners2, ret)
        print(objp)
    output = img.copy()
    # detect circles in the image
    
    '''
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 10)
    # ensure at least some circles were found
    if circles is not None:
    	# convert the (x, y) coordinates and radius of the circles to integers
    	circles = np.round(circles[0, :]).astype("int")
    	# loop over the (x, y) coordinates and radius of the circles
    	for (x, y, r) in circles:
    		# draw the circle in the output image, then draw a rectangle
    		# corresponding to the center of the circle
    		cv.circle(output, (x, y), r, (0, 255, 0), 4)
    		cv.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    	# show the output image
    	cv.imshow("Circle output", np.hstack([img, output]))
    '''
    
    cv.imshow('img', img)
    cv.waitKey(1)
cv.waitKey(1)
cv.destroyAllWindows()
cv.waitKey(1)
