import cv2
import numpy as np
import matplotlib.pyplot as plt
from match_template import match_template
import matplotlib.patches as patches
from Utils import *

from time import time

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

img_path = 'Fastest_Image_Pattern_Matching/Test Images/Src1.bmp'
template_path = 'Fastest_Image_Pattern_Matching/Test Images/20220611.bmp'
# template_path = 'Fastest_Image_Pattern_Matching/Test Images/Dst4.bmp'

img = cv2.imread(img_path, 1)
template = cv2.imread(template_path, 1)

number_pyramids = 4
threshold = 0.9
overlap = 0.5
method = methods[3]

points = []

start = time()
layer = img
img_pyramid = []
for _ in range(number_pyramids):
    img_pyramid.append(layer)
    layer = cv2.pyrDown(layer)

layer = template
template_pyramid = []
for _ in range(number_pyramids):
    template_pyramid.append(layer)
    layer = cv2.pyrDown(layer)

img_pyramid, template_pyramid = img_pyramid[::-1], template_pyramid[::-1]

points = []
for next_angle in range(0, 360, 2):
    for next_scale in range(100, 101, 1):
        point = match_template(img_pyramid[0], template_pyramid[0], method, next_angle, next_scale, threshold)
        points.append(point)

points = list(filter(None, points))
points = non_max_suppression_fast(points, overlap)
# new_threshold = sorted(points, key=lambda x: x[4])[0][4]

for idx in range(1, len(img_pyramid)):
    receptive_points = []
    for point in points:
        rotated_template, mask, x, y = rotate_template(template_pyramid[idx], point[2])
        roi = img_pyramid[idx][int(point[1])*2-2:int(point[1]*2+y+2), int(point[0])*2-2:int(point[0]*2+x+2)]
        try:
            receptive_point = match_template(roi, template_pyramid[idx], method, point[2], point[3], threshold)
        except:
            continue
        if receptive_point is None:
            continue
        receptive_point[0], receptive_point[1] = receptive_point[0]+point[0]*2-2, receptive_point[1]+point[1]*2-2
        receptive_points.append(receptive_point)
    
    del points
    points = receptive_points
    points = non_max_suppression_fast(points, overlap)
    # new_threshold = sorted(points, key=lambda x: x[4])[0][4]

print(np.round(points, 3))
end = time()
print(f'time: {end-start}')

fig, ax = plt.subplots(1)
ax.imshow(img_pyramid[-1])

for point_info in points:
    point = point_info[0], point_info[1]
    width = point_info[5]
    height = point_info[6]

    plt.scatter(point[0] + (width/2), point[1] + (height/2), s=20, color="red")
    box = patches.Rectangle((point[0], point[1]), width, height, color="green", alpha=0.50, label='Bounding box')
    ax.add_patch(box)
    plt.legend(handles=[box])

plt.show()