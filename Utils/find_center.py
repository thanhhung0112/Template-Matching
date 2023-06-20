import cv2
import numpy as np
import matplotlib.pyplot as plt
from Utils.image_processing_algorithms import *
import logging

logger = logging.getLogger(__name__)

def compute_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def find_center(img_gray, bbox, intensity_of_template_gray):
    (x1, y1, w, h) = bbox
    x2, y2 = x1 + w, y1 + h
    
    roi_gray = img_gray[y1:y2, x1:x2]
    padded_roi_gray = img_gray[y1-100:y2+100, x1-100:x2+100]
    
    roi_gray, padded_roi_gray = list(map(lambda x: contrast_stretching(x, {"low_clip": 10, "high_clip": 90}), [roi_gray, padded_roi_gray]))
    _, roi_gray = cv2.threshold(roi_gray, 100, 255, cv2.THRESH_BINARY_INV)
    _, padded_roi_gray = cv2.threshold(padded_roi_gray, 100, 255, cv2.THRESH_BINARY_INV)
    
    intensity_of_roi_gray = np.sum(padded_roi_gray == 0)
    possible_grasp_ratio = intensity_of_roi_gray / intensity_of_template_gray
    
    # find canny edges
    edges = cv2.Canny(roi_gray, 100, 200)
    edges = cv2.dilate(edges, np.ones((2, 2), np.uint8))
    
    # find contours from edges
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    distances_circle = []
    for contour in contours:
        if cv2.minAreaRect(contour)[1][0] * cv2.minAreaRect(contour)[1][1] > roi_gray.shape[0] * roi_gray.shape[1] / 8:
            continue

        try:
            if (cv2.minAreaRect(contour)[1][0] / cv2.minAreaRect(contour)[1][1] > 1.25) or (cv2.minAreaRect(contour)[1][0] / cv2.minAreaRect(contour)[1][1] < 0.75):
                continue
        except Exception as e:
            # logger.exception(f'Filter contour: {e}\n')
            continue

        if len(contour) < 50: #fine tune
            continue
        
        # create circle from contour
        (center_x_c, center_y_c), radious = cv2.minEnclosingCircle(contour)
        distances_circle.append({"center":(center_x_c, center_y_c), "radious":radious, "contour": contour})
    
    distances_circle = sorted(distances_circle, key=lambda x:x["radious"])
    
    try:
        centroid = np.mean(distances_circle[0]["contour"], axis=0)
        centroid_x = centroid[0][0]
        centroid_y = centroid[0][1]
    except Exception as e:
        logger.error(f'No contour found\n')

    center_c_x, center_c_y = distances_circle[0]["center"]  # center of circle    
    
    true_center_x, true_center_y = (0.5*centroid_x + 0.5*center_c_x), (0.5*centroid_y + 0.5*center_c_y)
    center_obj = (true_center_x+x1, true_center_y+y1)

    return center_obj, possible_grasp_ratio