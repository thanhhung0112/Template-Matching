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

def find_center(img_gray, bbox):
    (x1, y1, w, h) = bbox
    x2, y2 = x1 + w, y1 + h
    center_b_x, center_b_y = (x2-x1)/2, (y2-y1)/2  # center of roi 
    roi_gray = img_gray[y1:y2, x1:x2]
    
    # find canny edges
    edges = cv2.Canny(roi_gray, 100, 200)
    edges = cv2.dilate(edges, np.ones((2, 2), np.uint8))
    
    # find contours from edges
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    # distances_ellipse = []
    distances_circle = []
    for contour in contours:
        if cv2.minAreaRect(contour)[1][0] * cv2.minAreaRect(contour)[1][1] > roi_gray.shape[0] * roi_gray.shape[1] / 8:
            continue

        try:
            if (cv2.minAreaRect(contour)[1][0] / cv2.minAreaRect(contour)[1][1] > 1.25) or (cv2.minAreaRect(contour)[1][0] / cv2.minAreaRect(contour)[1][1] < 0.75):
                continue
        except Exception as e:
            logger.exception(f'Filter contour: {e}\n')

        if len(contour) < 50: #fine tune
            continue
        
        # create ellipse from contour
        # ellipse = cv2.fitEllipse(contour)
        # center_x_e, center_y_e = ellipse[0]
        # ellipse_w, ellipse_h = ellipse[1][0], ellipse[1][1]
        # distance_e = compute_distance((center_b_x, center_b_y), (center_x_e, center_y_e))
        # distances_ellipse.append({"center":(center_x_e, center_y_e), "distance":distance_e, "height":ellipse_h})
        
        # create circle from contour
        (center_x_c, center_y_c), radious = cv2.minEnclosingCircle(contour)
        distance_c = compute_distance((center_b_x, center_b_y), (center_x_c, center_y_c))
        distances_circle.append({"center":(center_x_c, center_y_c), "distance":distance_c, "radious":radious, "contour": contour})
    
    # distances_ellipse = sorted(distances_ellipse, key=lambda x:x["distance"])
    
    distances_circle = sorted(distances_circle, key=lambda x:x["radious"])
    
    try:
        centroid = np.mean(distances_circle[0]["contour"], axis=0)
        centroid_x = centroid[0][0]
        centroid_y = centroid[0][1]
    except Exception as e:
        logger.error(f'No contour found\n')

    # center_e_x, center_e_y = distances_ellipse[0]["center"]   # center of ellipse
    center_c_x, center_c_y = distances_circle[0]["center"]  # center of circle
    
    # find center of object on roi
    # true_center_x, true_center_y = (0.1*center_e_x+0.9*center_c_x), (0.1*center_e_y+0.9*center_c_y)
    
    true_center_x, true_center_y = (0.5*centroid_x + 0.5*center_c_x), (0.5*centroid_y + 0.5*center_c_y)
    center_obj = (true_center_x+x1, true_center_y+y1)

    return center_obj