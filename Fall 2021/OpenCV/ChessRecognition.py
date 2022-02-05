import numpy as np
import cv2 as cv

def extendChessboard(conners):
    newCorners = np.zeros((81, 1, 2), np.float32)
    for index, pair in enumerate(conners):
        pair = pair[0]
        row, col = indexToRowCol(index, (7,7))
        row += 1
        col += 1
        newIndex = rowColToIndex(row, col, (9,9))
        newCorners[newIndex][0] = pair
    # Manually extend the edge    
    newCorners[0][0] = 2 * corners[0][0] - corners[8][0]
    newCorners[8][0] = 2 * corners[6][0] - corners[12][0]
    newCorners[72][0] = 2 * corners[42][0] - corners[36][0]
    newCorners[80][0] = 2 * corners[48][0] - corners[40][0]
    # extend the row
    row = 0
    for col in range(1,8):
        i = rowColToIndex(row, col, (9,9))
        i_1 = rowColToIndex(row, col-1, (7,7))
        i_2 = rowColToIndex(row+1, col-1, (7,7))
        newCorners[i][0] = 2 * corners[i_1][0] - corners[i_2][0]
    row = 8
    for col in range(1,8):
        i = rowColToIndex(row, col, (9,9))
        i_1 = rowColToIndex(row-2, col-1, (7,7))
        i_2 = rowColToIndex(row-3, col-1, (7,7))
        newCorners[i][0] = 2 * corners[i_1][0] - corners[i_2][0]
    return newCorners

def indexToRowCol(index,size):
    c_count = size[1]

    row = index // c_count
    column = index % c_count
    return row, column

def rowColToIndex(row, col, size):
    col_count = size[1]
    
    index = row * col_count + col
    return index

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
    ret, corners = cv.findChessboardCorners(gray, (7, 7), None, cv.CALIB_CB_FAST_CHECK)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        newCorners = extendChessboard(corners)
        
        print(corners)
        print(f"Conners size = {corners.shape} {corners.dtype}")
        print("\n\n\n")
        print(newCorners)
        print(f"NewConners size = {newCorners.shape}")
        print("\n\n\n")
        
        # Draw and display the corners
        #cv.drawChessboardCorners(img, (7,7), corners2, ret)
        cv.drawChessboardCorners(img, (9,9), newCorners, ret)
    output = img.copy()

    cv.imshow('img', img)
    key = cv.waitKey(50)
    if key != -1:
        if key == 113:
            break
        else:
            print(key)
            break
cv.waitKey(1)
cv.destroyAllWindows()
cv.waitKey(1)