from ultralytics import YOLO
import cv2
import numpy as np

def instance_segment(image, model, conf):
    result = model.predict(source=image, show=False, save=False)
    contours = result[0].masks.xy

    mask = np.zeros(shape=(image.shape[:2]))
    for idx, cnt in enumerate(contours):
        cnt = cnt.astype(np.int32)
        cv2.drawContours(mask, [cnt], 0, idx, cv2.FILLED)

    return mask