import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import local_binary_pattern

# Load the image
img = cv2.imread("Dataset/Dst1.bmp", 0)

# Define the LBP operator
radius = 10
n_points = 8 * radius
lbp = local_binary_pattern(img, n_points, radius, 'uniform')
lbp = np.uint8(lbp)

plt.imshow(lbp)
plt.show()