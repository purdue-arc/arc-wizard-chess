import cv2

DICTIONARY_TYPE = cv2.aruco.DICT_7X7_50

WC_CV_DIRECTORY = "Spring 2023/Computer Vision/"
TAGS_DIRECTORY = WC_CV_DIRECTORY + "tags/"
CAMERA_MATRIX_PATH = WC_CV_DIRECTORY + "camera_matrix.npy"
DISTORTION_COEFFS_PATH = WC_CV_DIRECTORY + "distortion_coefficients.npy"

"""
0-7: w-pawns
8: w-queen
9: w-king
20,21: w-rooks
30,31: w-knights
40,41: w-bishops
10-17: b-pawns
18: b-queen
19: b-king
22,23: b-rooks
32,33: b-knights
42,43: b-bishops
"""
PIECE_IDS = dict()
PIECE_IDS.update({i: f"w-pawn-{i}" for i in range(8)})
PIECE_IDS.update({i + 10: f"b-pawn-{i}" for i in range(8)})
PIECE_IDS.update({i + 20: f"w-rook-{i}" for i in range(2)})
PIECE_IDS.update({i + 22: f"b-rook-{i}" for i in range(2)})
PIECE_IDS.update({i + 30: f"w-knight-{i}" for i in range(2)})
PIECE_IDS.update({i + 32: f"b-knight-{i}" for i in range(2)})
PIECE_IDS.update({i + 40: f"w-bishop-{i}" for i in range(2)})
PIECE_IDS.update({i + 42: f"b-bishop-{i}" for i in range(2)})
PIECE_IDS.update({
    8: "w-queen",
    9: "w-king",
    18: "b-queen",
    19: "b-king"
})