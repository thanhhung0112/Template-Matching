import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from time import time
from rembg import remove

def proposal_roi(image, temp):
    if len(image.shape) == 3:
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(temp.shape) == 3:
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

    area_temp = temp.shape[0] * temp.shape[1]

    new_img = remove(img_gray)
    new_img = cv2.cvtColor(new_img, cv2.COLOR_BGRA2GRAY)

    new_img = pixel_duplicate(new_img, ratio=0.75)
    new_img = cv2.addWeighted(img_gray, 0.75, new_img, 2.5, 0)
    new_img = sharpen(new_img)

    hist = cv2.calcHist([new_img], [0], None, [256], [0, 256])
    score, _ = cv2.threshold(new_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_TRIANGLE)
    score = int(score)
    peak1 = np.argmax(hist.T[0][:score])
    peak2 = np.argmax(hist.T[0][score:]) + score
    
    if peak2 == 255:
        _, mask = cv2.threshold(new_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)

        _, labels, stats_img, _ = cv2.connectedComponentsWithStats(mask)
        areas_img = stats_img[:, 4]

        binary = np.zeros_like(mask)

        mask = (areas_img[1:] >= area_temp/10) & (areas_img[1:] <= area_temp*1.5)
        indices = np.where(mask)[0] + 1
        binary[np.isin(labels, indices)] = 255
    
    else:
        _, mask = cv2.threshold(new_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_TRIANGLE)

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)

        _, labels, stats_img, _ = cv2.connectedComponentsWithStats(mask)
        areas_img = stats_img[:, 4]

        binary = np.zeros_like(mask)

        mask = (areas_img[1:] >= area_temp/10) & (areas_img[1:] <= area_temp*1.5)
        indices = np.where(mask)[0] + 1
        binary[np.isin(labels, indices)] = 255

    _, labels_img = cv2.connectedComponents(binary)
    del stats_img
    # del binary

    labels_img = labels_img.reshape(labels_img.shape[0], labels_img.shape[1], 1)
    obj_ids = np.unique(labels_img)
    num_objs = len(obj_ids)

    boxes = []
    object_roi = np.zeros_like(img_gray)
    for i in range(1, num_objs):
        binary_mask = np.all(labels_img==obj_ids[i], axis=2)
        binary_mask = binary_mask.astype(np.uint8)

        points = cv2.findNonZero(binary_mask)
        del binary_mask
        
        box = cv2.boundingRect(points)
        rect = cv2.minAreaRect(points)
        corner = cv2.boxPoints(rect)
        corner = np.int0(corner)
        cv2.drawContours(object_roi, [corner], -1, 255, cv2.FILLED)

        del points

        angle = rect[2], rect[2]+90, rect[2]+180, rect[2]+270
        boxes.append([box, angle])

    # for box, angle in boxes:
    #     cv2.rectangle(image, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0, 255, 0), 6)

    # plt.imshow(image)
    # plt.show()

    del labels_img
    return boxes, binary

# img_path = 'Dataset/custom.jpg'
# template_path = 'Dataset/template_custom.jpg'

# img_path = 'Dataset/Src1.bmp'
# template_path = 'Dataset/Dst1.bmp'

# img_path = 'Dataset/Src10.bmp'
# template_path = 'Dataset/Dst10.jpg'

# img = cv2.imread(img_path, 1)
# template = cv2.imread(template_path, 1)
# boxes, object_roi = proposal_roi(img, template)