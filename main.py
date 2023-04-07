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

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

img_path = 'Dataset/custom.jpg'
template_path = 'Dataset/template_custom.jpg'
# img_path = 'Dataset/Src1.bmp'
# template_path = 'Dataset/20220611.bmp'

threshold = 0.75
overlap = 0.5
method = methods[3]

img = cv2.imread(img_path, 1)
template = cv2.imread(template_path, 1)
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

start = time()

boxes, object_roi = proposal_roi(img, template)

# print(boxes)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

mask = np.zeros_like(img_gray)
mask = cv2.bitwise_and(img_gray, object_roi)
# img_gray = filter_clahe(img_gray, cliplimit=3, titleGridSize=8)
img_gray = cv2.addWeighted(img_gray, 1, mask, 0.25, 0)
img_gray = cv2.bitwise_and(img_gray, object_roi)
# plt.imshow(img_gray)
# plt.show()
# v[0] = 1

end = time()
time_proposal = end - start

start = time()
good_points = []
for box, angle in boxes:
    for next_angle in angle:
        for sub_angle in [next_angle, next_angle+1, next_angle+2, next_angle+3]:
            temp_new, _, w_temp, h_temp = rotate_template(template, next_angle)
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
            print(roi.shape, template.shape)
            if roi.shape[0]*roi.shape[1] > w_temp*h_temp*5:
                break

            try:
                point = match_template(roi, template, method, sub_angle, 100, threshold)
                print(point)
            except:
                continue

            if point is None:
                continue
            
            # cv2.rectangle(roi, (point[0], point[1]), (point[0]+point[5], point[1]+point[6]), 255, 3)
            # plt.subplot(1, 2, 1)
            # plt.imshow(roi)
            # plt.subplot(1, 2, 2)
            # plt.imshow(temp_new)
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