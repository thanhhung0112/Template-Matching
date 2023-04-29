import cv2
import numpy as np
import matplotlib.pyplot as plt

from Utils import *

def match_template(img, template, method, rot, scale, matched_thresh):
    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
        
    if len(template.shape) == 3:
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    else:
        template_gray = template

    h, w = template_gray.shape

    if rot == 0:
        mask = np.full((h, w, 1), (255), dtype=np.uint8)
        rotated_template = template_gray
        new_w, new_h = w, h
    else:
        rotated_template, mask, new_w, new_h = rotate_template(template_gray, rot)

    method = eval(method)

    if (img_gray.shape[0] < rotated_template.shape[0]) or (img_gray.shape[1] < rotated_template.shape[1]):
        return
    
    # start = time()
    matched_points = cv2.matchTemplate(img_gray, rotated_template, method, None, mask)
    # end = time()
    # print(f'time: {end-start}')

    _, max_val, _, max_loc = cv2.minMaxLoc(matched_points)

    if max_val >= matched_thresh and max_val <= 1.0:
        return [*max_loc, rot, scale, max_val, new_w, new_h]
