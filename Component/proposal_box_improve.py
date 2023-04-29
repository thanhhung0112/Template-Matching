import cv2
import numpy as np
import matplotlib.pyplot as plt
from Utils import *
import json

def proposal_roi(image, temp, enhance_algorithms=None):
    if len(image.shape) == 3:
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(temp.shape) == 3:
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    area_temp = temp.shape[0] * temp.shape[1]

    enhanced_img = image
    for key, value in enhance_algorithms.items():
        func = eval(key)
        enhanced_img = func(enhanced_img, value)
        # plt.imshow(enhanced_img)
        # plt.show()

    enhanced_img = remove_wrong_contours(enhanced_img, area_temp, selection_area=[0.1, 1.5])

    _, labels_img = cv2.connectedComponents(enhanced_img)

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
    #     cv2.rectangle(image, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0), 6)

    # plt.imshow(image)
    # plt.show()

    del labels_img
    return boxes, enhanced_img

if __name__ == '__main__':
    img_path = 'Dataset/Src10.bmp'
    template_path = 'Dataset/Dst10.jpg'

    img = cv2.imread(img_path, 1)
    template = cv2.imread(template_path, 1)

    with open('Custom_enhance/Src3-5-8-9-10.json', 'r') as file:
        enhance_algorithms = json.load(file)

    boxes, object_roi = proposal_roi(img, template, enhance_algorithms=enhance_algorithms)