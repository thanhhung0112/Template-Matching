import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils import *
from proposal_box_improve import proposal_roi
from match_template import match_template
from non_max_suppression import non_max_suppression_fast
from rotate_template import rotate_template
from image_representation import image_representation
from time import time
import json
from export_csv import export_csv

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# img_path = '/home/kratos/code/Capstone/Demo-model-AI/Template-Matching/Dataset/custom2.jpg'
# template_path = '/home/kratos/code/Capstone/Demo-model-AI/Template-Matching/Dataset/template_custom.jpg'
# img_path = 'Dataset/Src1.bmp'
# template_path = 'Dataset/20220611.bmp'

img_path = '/home/kratos/code/Capstone/Demo-model-AI/Template-Matching/Dataset/Src3.bmp'
template_path = '/home/kratos/code/Capstone/Demo-model-AI/Template-Matching/Dataset/Dst3.bmp'

custom_enhance_algorithms_path = '/home/kratos/code/Capstone/Demo-model-AI/Template-Matching/Custom_enhance/Src3-5-8-9-10.json'
custom_representation = '/home/kratos/code/Capstone/Demo-model-AI/Template-Matching/Custom_representation/Src3-5-8-9-10.json'

threshold = 0.97
overlap = 0.4
modify_angle = np.arange(-1, 1, 1)
method = methods[3]

img = cv2.imread(img_path, 1)
template = cv2.imread(template_path, 1)

with open(custom_representation, 'r') as file:
    representation_algorithms = json.load(file)

template_gray = image_representation(template, target='template', representation_algorithms=representation_algorithms)

start = time()

with open(custom_enhance_algorithms_path, 'r') as file:
        enhance_algorithms = json.load(file)
boxes, object_roi = proposal_roi(img, template, enhance_algorithms=enhance_algorithms)

img_gray = image_representation(img, target='target_image', representation_algorithms=representation_algorithms)

end = time()
time_proposal = end - start

start = time()
good_points = []
for box, angle in boxes:
    for next_angle in angle:
        sub_angles = next_angle + modify_angle
        for sub_angle in sub_angles:
            temp_new, _, w_temp, h_temp = rotate_template(template_gray, sub_angle)
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

            # plt.subplot(1, 2, 1)
            # plt.imshow(roi)
            # plt.subplot(1, 2, 2)
            # plt.imshow(temp_new)
            # plt.show()

            if roi.shape[0]*roi.shape[1] > w_temp*h_temp*5:
                continue

            try:
                point = match_template(roi, template_gray, method, sub_angle, 100, threshold)
                print('Point: ', point)
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
# print(np.round(good_points, 3))
export_csv(good_points)
print(f'found {len(good_points)} objects')
print(f'time proposal: {time_proposal}')
print(f'time match: {end-start}')

fig, ax = plt.subplots(1)
ax.imshow(img)

for point_info in good_points:
    point = point_info[0], point_info[1]
    width = point_info[5]
    height = point_info[6]

    # plt.scatter(point[0] + (width/2), point[1] + (height/2), s=20, color="red")
    # box = patches.Rectangle((point[0], point[1]), width, height, color="green", alpha=0.50, label='Bounding box')
    # ax.add_patch(box)
    # plt.legend(handles=[box])
    cv2.circle(img, (int(point[0]+width/2), int(point[1]+height/2)), 3, (0, 0, 255), 7)
    cv2.rectangle(img, (int(point[0]), int(point[1])), (int(point[0]+width), int(point[1]+height)), (0, 255, 0), 3)

cv2.imwrite('/home/kratos/code/Capstone/Demo-model-AI/Template-Matching/Output/output.jpg', img)
# plt.imshow(img)
# plt.show()