import cv2
import time
import wc_constants as wc

# B, G, R
outline_color = (0, 200, 0)
center_color = (0, 0, 200)
text_color = (200, 100, 0)

def display_aruco(corners, ids, image):
    # check if at least one marker detected
    if len(corners) > 0:
        # flatten marker id list
        ids = ids.flatten()

        for marker_corner, market_id in zip(corners, ids):
            # dim 4x2 - 4 corner points per marker, 2 coords (x,y) per point
            print(marker_corner.shape[1])
            corners = marker_corner.reshape((4, 2))   
            top_left, top_right, bot_right, bot_left = corners

            # convert point coordinates to integers
            top_left = (int(top_left[0]), int(top_left[1]))
            top_right = (int(top_right[0]), int(top_right[1]))
            bot_right = (int(bot_right[0]), int(bot_right[1]))
            bot_left = (int(bot_left[0]), int(bot_left[1]))

            # draw outline of marker on image
            cv2.line(image, top_left, top_right, outline_color, 2)
            cv2.line(image, top_right, bot_right, outline_color, 2)
            cv2.line(image, bot_right, bot_left, outline_color, 2)
            cv2.line(image, bot_left, top_left, outline_color, 2)

            # compute and draw center of marker
            cX = int((top_left[0] + bot_right[0]) / 2.0)
            cY = int((top_left[1] + bot_right[1]) / 2.0)
            cv2.circle(image, (cX, cY), 4, center_color, -1)

            # draw the marker id on the image
            cv2.putText(image, wc.PIECE_IDS[market_id],
                (top_left[0], top_left[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, text_color, 2)
    return image


def main():
    detector_params = cv2.aruco.DetectorParameters()
    dictionary = cv2.aruco.getPredefinedDictionary(wc.DICTIONARY_TYPE)
    detector = cv2.aruco.ArucoDetector(dictionary, detector_params)

    # initialize video capture object
    capture = cv2.VideoCapture(0)

    while True:
        # capture frame
        ret, frame = capture.read()

        # detect aruco markers in frame
        corners, ids, rejected = detector.detectMarkers(frame)

        # draw aruco marker bounds and labels onto image
        image = display_aruco(corners, ids, frame)
        
        # display video in new window
        cv2.imshow("Video", image)
        
        # stop video capture when q is pressed
        key = cv2.waitKey(20)
        if key == ord('q'):
            break

    # stop video capture
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()