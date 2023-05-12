from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt

def instance_segment(image, model, conf=0.7):
    result = model.predict(source=image, show=False, save=False, conf=conf)
    contours = result[0].masks.xy

    mask = np.zeros(shape=(image.shape[:2]))
    for idx, cnt in enumerate(contours):
        cnt = cnt.astype(np.int32)
        cv2.drawContours(mask, [cnt], 0, idx+1, cv2.FILLED)

    return mask

if __name__ == '__main__':
    model = YOLO('Weights/last.pt')
    img = cv2.imread('Dataset/Src5-0.bmp')
    mask = instance_segment(img, model, conf=0.25)
    plt.imshow(mask, cmap='gray')
    plt.show()