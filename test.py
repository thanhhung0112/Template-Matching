import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import *

# Read the image and convert to grayscale
img = cv2.imread ("Dataset/Src10.bmp")
gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)

temp = cv2.imread ("Dataset/Dst10.jpg", 1)
area_temp = temp.shape[0] * temp.shape[1]

new_img = gamma_correction(gray, gamma=0.5)
new_img = remove_shadow(new_img)
new_img = sharpen(new_img)
mask = cv2.cvtColor(new_img, cv2.COLOR_GRAY2BGR)
plt.imshow(new_img)
plt.show()

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilation = cv2.dilate(new_img, kernel, iterations=5)
plt.imshow(dilation)
plt.show()

erosion = cv2.erode(dilation, kernel, iterations=5)
plt.imshow(erosion)
plt.show()

dist = cv2.distanceTransform (new_img, cv2.DIST_L2, 5)
plt.imshow(dist)
plt.show()

cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
# plt.imshow(dist)
# plt.show()

_, dist = cv2.threshold(dist, 0.2, 1.0, cv2.THRESH_BINARY)
plt.imshow(dist)
plt.show()

kernel1 = np.ones((3,3), dtype=np.uint8)
dist = cv2.dilate(dist, kernel1)
# plt.imshow(dist)
# plt.show()

dist_8u = dist.astype('uint8')

_, labels, stats_img, _ = cv2.connectedComponentsWithStats(dist_8u)
areas_img = stats_img[:, 4]
output = np.zeros_like(new_img)
mask = areas_img[1:] >= area_temp/10
indices = np.where(mask)[0] + 1
output[np.isin(labels, indices)] = 255
# plt.imshow(output)
# plt.show()

_, labels_img = cv2.connectedComponents(output)
plt.imshow(labels_img)
plt.show()
# print(output.dtype)

labels_img = cv2.watershed(mask, labels_img)
plt.imshow(labels_img)
plt.show()

# labels_img = labels_img.reshape(labels_img.shape[0], labels_img.shape[1], 1)
# obj_ids = np.unique(labels_img)
# num_objs = len(obj_ids)

# boxes = []
# for i in range(num_objs):
#     binary_mask = np.all(labels_img==obj_ids[i], axis=2)
#     binary_mask = binary_mask.astype(np.uint8)

#     points = cv2.findNonZero(binary_mask)
#     del binary_mask

#     box = cv2.boundingRect(points)
#     rect = cv2.minAreaRect(points)
#     del points

#     angle = rect[2], rect[2]+180, rect[2]+90, rect[2]+90+180

#     if box[2] > temp.shape[1]*4 or box[3] > temp.shape[0]*4:
#         continue
#     boxes.append([box, angle])

# for box, angle in boxes:
#     cv2.rectangle(img, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0, 255, 0), 4)

# plt.imshow(img)
# plt.show()

