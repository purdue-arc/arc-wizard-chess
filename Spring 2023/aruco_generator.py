import numpy as np
import cv2

import wc_constants as wc

def generate_marker(dict_type, id, image_size, output_file=f"{id}.png"):
    # load specified aruco dictionary 
    dict = cv2.aruco.getPredefinedDictionary(dict_type)

    # create array to draw aruco marker onto
    tag = np.zeros((image_size, image_size, 1), dtype="uint8")

    # draw aruco marker onto tag array
    cv2.aruco.generateImageMarker(dict, id, image_size, tag, 1)

    # save marker image to disk
    cv2.imwrite(output_file, tag)

def generate_all_chess_markers():
    for id in wc.PIECE_IDS:
        generate_marker(wc.DICTIONARY_TYPE, id, 800, f"{wc.TAGS_DIRECTORY}{wc.PIECE_IDS[id]}.png")

if __name__ == "__main__":
    generate_all_chess_markers()