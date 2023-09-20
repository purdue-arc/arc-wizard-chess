import cv2
import numpy as np

import wc_constants as wc

import camera

def estimate_pose(frame, dict_type, camera_matrix, distortion_coeffs, marker_length): # marker_length in meters prolly
    # set coordinate system (3d physical points that 2d image points map to)
    obj_points = np.array(
        [[-marker_length / 2, marker_length / 2, 0],
         [marker_length / 2, marker_length / 2, 0],
         [marker_length / 2, -marker_length / 2, 0],
         [-marker_length / 2, -marker_length / 2, 0]]
    )

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    aruco_dict = cv2.aruco.getPredefinedDictionary(dict_type)
    detector_params = cv2.aruco.DetectorParameters()
    aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, detector_params)

    # undistort image using matrix and dist coefficients
    # gray = cv2.undistort(gray, camera_matrix, distortion_coeffs) # maybe not needed?

    # detect aruco markers in image
    corners, ids, rejected = aruco_detector.detectMarkers(gray)

    if len(corners) > 0:
        # mapping from piece id to tuple (rvec, tvec)
        poses = dict()

        # loop through each marker detected
        for i, marker_id in enumerate(ids):
            # generate rotation and translation vectors from marker to camera
            ret, rvec, tvec = cv2.solvePnP(obj_points, corners[i], camera_matrix, distortion_coeffs, cv2.SOLVEPNP_IPPE_SQUARE)
            # rvec, tvec = cv2.solvePnPRefineLM(obj_points, corners[i], camera_matrix, distortion_coeffs, rvec, tvec)
            # rvec, tvec = cv2.solvePnPRefineVVS(obj_points, corners[i], camera_matrix, distortion_coeffs, rvec, tvec)

            frame = cv2.drawFrameAxes(frame, camera_matrix, distortion_coeffs, rvec, tvec, 0.1)
            # map corresponding piece id to these vectors
            print(f"\rrvec: {rvec[0]}, {rvec[1]}, {rvec[2]},   tvec: {tvec[0]}, {tvec[1]}, {tvec[2]}", end="")
            
            # poses[wc.PIECE_IDS[marker_id]] = (rvec, tvec)
        # draw axes for each marker
        # for piece_id in poses:
        #     rvec, tvec = poses[piece_id]
        #     frame = cv2.drawFrameAxes(frame, camera_matrix, distortion_coeffs, rvec, tvec, 0.1)
    else:
        print("\rNo markers detected!", end="")

    # frame = gray
    return camera.display_aruco(corners, ids, frame)


def main():
    # load camera matrix and distortion coefficients from files
    camera_matrix = np.load(wc.CAMERA_MATRIX_PATH)
    dist_coeffs = np.load(wc.DISTORTION_COEFFS_PATH)

    # initialize video capture object
    capture = cv2.VideoCapture(0)

    while True:
        # capture frame
        ret, frame = capture.read()

        image = estimate_pose(frame, wc.DICTIONARY_TYPE, camera_matrix, dist_coeffs, 0.3) # marker length in meters?

        cv2.imshow("Pose Estimation Videofeed", image)

        # stop video capture when q is pressed
        key = cv2.waitKey(20)
        if key == ord('q'):
            break


if __name__ == "__main__":
    main()