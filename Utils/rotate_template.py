import cv2
import numpy as np
import matplotlib.pyplot as plt

def rotate_template(image, angle):
    h, w = image.shape[:2]
    cx, cy = (w // 2, h // 2)

    # get rotation matrix (explained in section below)
    M = cv2.getRotationMatrix2D((cx, cy), -angle, 1.0)

    # get cos and sin value from the rotation matrix
    cos, sin = abs(M[0, 0]), abs(M[0, 1])

    # calculate new width and height after rotation (explained in section below)
    newW = int((h * sin) + (w * cos))
    newH = int((h * cos) + (w * sin))

    # calculate new rotation center
    M[0, 2] += (newW / 2) - cx
    M[1, 2] += (newH / 2) - cy

    # use modified rotation center and rotation matrix in the warpAffine method
    result = cv2.warpAffine(image,
                            M, (newW, newH),
                            borderValue=(0, 0, 0),
                            flags=cv2.INTER_LINEAR)

    pixel_array = np.full((h, w, 1), (255), dtype=np.uint8)
    mask = cv2.warpAffine(pixel_array, M, (newW, newH))

    return result, mask, newW, newH