# short_desc: mask to polygon
import numpy as np
import cv2


def mask_to_polygon(mask):
    if not isinstance(mask, np.ndarray):
        mask = np.array(mask).astype('uint8')

    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    # H, W = mask.shape[:2]
    polygons = tuple(c[:, 0, :] for c in contours)

    return polygons
