import cv2
import numpy as np
import sys

import wc_constants as wc

def capture_viewpoints(cam_num=0, num_frames=1, size=None):
    frames = []

    capture = cv2.VideoCapture(cam_num)

    while True:
        ret, frame = capture.read()

        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)

        cv2.imshow("Calibration Viewpoint Capture", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == 10 or key == 32:  # Enter or Space
            frames.append(frame)
            print("Frame captured!")
            if len(frames) == num_frames:
                break

    return frames

def read_chessboards(frames, dict_type, board):
    detector_params = cv2.aruco.DetectorParameters()
    aruco_dict = cv2.aruco.getPredefinedDictionary(dict_type)
    aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, detector_params)

    # charuco_params = cv2.aruco.CharucoParameters()
    # charuco_detector = cv2.aruco.CharucoDetector(board)

    all_corners = []
    all_ids = []

    for frame in frames:
        # grayscale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # find aruco markers in image
        m_corners, m_ids, rejected = aruco_detector.detectMarkers(gray)

        # check if at least one aruco marker detected
        if len(m_corners) > 0:
            # get charuco corners and ids from detected aruco markers
            ret, c_corners, c_ids = cv2.aruco.interpolateCornersCharuco(m_corners, m_ids, gray, board)   #IMPORTANT to DETECT
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.01)
            ret, c_ids = cv2.aruco.calibrateCameraCharuco(m_corners, )
            c_corners = np.array(m_corners, dtype='float32')
            cv2.cornerSubPix(gray, c_corners, (5,5), (-1,-1), criteria)
            # c_corners, c_ids, _, _ = charuco_detector.detectBoard(gray, c_corners, c_ids, m_corners, m_ids)
            print(c_corners)
  
            # check if at least one charuco corner interpolated
            if ret > 0:
                all_corners.append(c_corners)
                all_ids.append(c_ids)
            else:
                print("Failed to find charuco corners")
        else:
            print("No markers detected!")

    # determine image size from frame
    img_size = gray.shape

    return all_corners, all_ids, img_size

def main():
    aruco_dict = cv2.aruco.getPredefinedDictionary(wc.DICTIONARY_TYPE)
    board = cv2.aruco.CharucoBoard((11, 8), 0.025, 0.019, aruco_dict) # squaresX, squaresY, squareLength (m), markerLength (m), dict

    # capture different views of board for calibration
    frames = capture_viewpoints(0, 50)
    if len(frames) == 0:
        print("No frames captured!")
        sys.exit(1)
    
    # get charuco corners and ids from captured frames
    charuco_corners, charuco_ids, img_size = read_chessboards(frames, wc.DICTIONARY_TYPE, board)

    if len(charuco_corners) > 0:
        # perform camera calibration on points 
        ret, camera_matrix, distortion_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
            charuco_corners, charuco_ids, board, img_size, None, None)

        # print matrix and distortion coefficients
        print("Camera matrix")
        print(camera_matrix)
        print("Distortion coefficients")
        print(distortion_coeffs)

        # save matrix and distortion coefficients in npy file
        np.save(wc.CAMERA_MATRIX_PATH, camera_matrix)
        np.save(wc.DISTORTION_COEFFS_PATH, distortion_coeffs)
    else:
        print("Calibration failed!")


if __name__ == "__main__":
    main()