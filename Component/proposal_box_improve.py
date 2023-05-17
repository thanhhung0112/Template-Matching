import cv2
import numpy as np
import matplotlib.pyplot as plt
from Utils import *
import json

def proposal_roi(image, temp, model, conf, enhance_algorithms=None):
    if len(image.shape) == 3:
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(temp.shape) == 3:
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    area_temp = temp.shape[0] * temp.shape[1]

    labels_img = instance_segment(image, model=model, conf=conf)
    
    # for key, value in enhance_algorithms.items():
    #     func = eval(key)
    #     labels_img = func(labels_img, value)
    #     # plt.imshow(labels_img)
    #     # plt.show()

    # labels_img = remove_wrong_contours(labels_img, area_temp, selection_area=[0.1, 1.5])

    # _, labels_img = cv2.connectedComponents(labels_img)

    labels_img = labels_img.reshape(labels_img.shape[0], labels_img.shape[1], 1)
    obj_ids = np.unique(labels_img)
    num_objs = len(obj_ids)

    boxes = []
    for i in range(1, num_objs):
        binary_mask = np.all(labels_img==obj_ids[i], axis=2)
        binary_mask = binary_mask.astype(np.uint8)

        points = cv2.findNonZero(binary_mask)
        del binary_mask
        
        box = cv2.boundingRect(points)
        angle = apply_min_area(points)
        del points

        boxes.append([box, angle])

    # for box, angle in boxes:
    #     cv2.rectangle(image, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0), 6)

    # plt.imshow(image)
    # plt.show()

    del labels_img
    return boxes