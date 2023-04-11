import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils import *
from proposal_box_improve import proposal_roi
from match_template import match_template
from non_max_suppression import non_max_suppression_fast
from rotate_template import rotate_template
from time import time
from skimage.feature import local_binary_pattern
import json

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# img_path = 'Dataset/custom.jpg'
# template_path = 'Dataset/template_custom.jpg'
img_path = 'Dataset/Src9.bmp'
template_path = 'Dataset/Dst8.bmp'
custom_enhance_algorithms_path = 'Custom_Algorithms/Src3-Src5.json'

threshold = 0.8
overlap = 0.5
modify_angle = np.arange(-4, 4, 2)
method = methods[1]

img = cv2.imread(img_path, 1)
template = cv2.imread(template_path, 1)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

start = time()

with open(custom_enhance_algorithms_path, 'r') as file:
        enhance_algorithms = json.load(file)
boxes, object_roi = proposal_roi(img, template, enhance_algorithms=enhance_algorithms)

# print(boxes)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

end = time()
time_proposal = end - start

start = time()
good_points = []
for box, angle in boxes:
    for next_angle in angle:
        sub_angles = next_angle + modify_angle
        for sub_angle in sub_angles:
            temp_new, _, w_temp, h_temp = rotate_template(template_gray, next_angle)
            epsilon_w, epsilon_h = np.abs([box[2]-w_temp, box[3]-h_temp])

            x_start, x_end = box[0]-epsilon_w, box[0]+box[2]+epsilon_w
            y_start, y_end = box[1]-epsilon_h, box[1]+box[3]+epsilon_h

            top = min(y_start, 0)
            left = min(x_start, 0)
            bottom = min(img_gray.shape[0]-y_end, 0)
            right = min(img_gray.shape[1]-x_end, 0)
            img_padded = cv2.copyMakeBorder(img_gray, abs(top), abs(bottom), abs(left), abs(right), cv2.BORDER_CONSTANT, value=0)

            roi = img_padded[y_start+abs(top):y_end+abs(top)+abs(bottom),
                            x_start+abs(left):x_end+abs(left)+abs(right)]
            
            # roi = cv2.medianBlur(roi, 15)
            # roi = laplacian_detect(roi, ksize=7)
            # _, roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
            # plt.subplot(1, 2, 1)
            # plt.imshow(roi)
            # plt.subplot(1, 2, 2)
            # plt.imshow(temp_new)
            # plt.show()
            print(roi.shape, template_gray.shape)
            if roi.shape[0]*roi.shape[1] > w_temp*h_temp*5:
                break

            try:
                point = match_template(roi, template_gray, method, sub_angle, 100, threshold)
                print(point)
            except:
                continue

            if point is None:
                continue
            
            # cv2.rectangle(roi, (point[0], point[1]), (point[0]+point[5], point[1]+point[6]), 255, 3)
            # plt.subplot(1, 2, 1)
            # plt.imshow(roi, cmap='gray')
            # plt.subplot(1, 2, 2)
            # plt.imshow(temp_new, cmap='gray')
            # plt.show()

            point[0], point[1] = point[0]+box[0]-epsilon_w, point[1]+box[1]-epsilon_h
            if (point[0] < 0):
                point[5] = point[5] - abs(point[0])
                point[0] = 0
            if (point[1] < 0):
                point[6] = point[6] - abs(point[1])
                point[1] = 0

            good_points.append(point)

try:
    good_points = non_max_suppression_fast(good_points, overlap)
except:
    print('No detection found')

end = time()
print(np.round(good_points, 3))
print(f'found {len(good_points)} objects')
print(f'time proposal: {time_proposal}')
print(f'time match: {end-start}')

fig, ax = plt.subplots(1)
ax.imshow(img)

for point_info in good_points:
    point = point_info[0], point_info[1]
    width = point_info[5]
    height = point_info[6]

    plt.scatter(point[0] + (width/2), point[1] + (height/2), s=20, color="red")
    box = patches.Rectangle((point[0], point[1]), width, height, color="green", alpha=0.50, label='Bounding box')
    ax.add_patch(box)
    plt.legend(handles=[box])

plt.show()