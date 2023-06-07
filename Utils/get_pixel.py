import math
import cv2 as cv
import numpy as np
import os
import argparse

# descStr = 'calc angle'
# parser = argparse.ArgumentParser(description=descStr)
# parser.add_argument('--img', dest='img', required=True)

# args = parser.parse_args()

# path = args.img_path

path = 'Dataset/test_custom_crop2.png'

img = cv.imread(path, 1)
points = []
def mouseEvent(eventName, x, y, flags, params):
    if eventName == cv.EVENT_LBUTTONDOWN:
        points.append([x, y])
        print(f'{x}, {y}')
        cv.circle(img, (x, y), 1, (255, 0, 0), -1)
        # cv.arrowedLine(img, tuple(points[0]), (x, y), (255, 0, 0), 3)
        cv.imshow('image', img)

while True:
    cv.imshow('image', img)
    cv.setMouseCallback('image', mouseEvent)
    if cv.waitKey(1) & 0xff == ord('e'):
        break
    if cv.getWindowProperty('image', cv.WND_PROP_VISIBLE) <1:
        break

cv.destroyAllWindows()