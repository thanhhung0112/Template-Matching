import cv2
import numpy as np
import matplotlib.pyplot as plt

points = []
temp = cv2.imread('Dataset/20220611.bmp')
rows, cols = temp.shape[:2]
M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)

def mouse_event(event_name, x, y, flags, params):
    if event_name == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        cv2.circle(temp, (x, y), 5, (255, 0, 0), -1)
        cv2.line(temp, tuple(points[-1]), (x, y), (255, 0, 0), 3)
        cv2.imshow('template', temp)


def custom_template(temp):
    while True:
        cv2.imshow('template', temp)
        cv2.setMouseCallback('template', mouse_event)
        if cv2.waitKey(1) & 0xff == ord('e'):
            break
        if cv2.getWindowProperty('template', cv2.WND_PROP_VISIBLE) <1:
            break

    cv2.destroyAllWindows()

custom_template(temp)
print(points)

# points = np.array([[46, 28], [117, 33], [161, 27], [276, 26], [213, 25], [326, 27], [382, 27], [439, 21], [494, 20], [544, 21], [584, 16], [627, 17], [657, 19], [690, 19], [720, 17], [736, 28], [749, 42], [768, 50], [822, 66], [861, 74], [893, 85], [955, 88], [1042, 82], [1095, 76], [1162, 71], [1194, 64], [1266, 58], [1317, 54], [1386, 49], [1450, 45], [1502, 52], [1555, 47], [1607, 47], [1657, 48], [1697, 52], [1761, 59], [1806, 59], [1839, 70], [1877, 80], [1891, 92], [1905, 126], [1904, 148], [1894, 171], [1884, 191], [1865, 203], [1841, 208], [1802, 209], [1770, 213], [1740, 222], [1692, 225], [1668, 226], [1614, 228], [1597, 228], [1583, 229], [1537, 233], [1511, 235], [1478, 233], [1459, 231], [1432, 231], [1386, 231], [1340, 232], [1308, 233], [1263, 231], [1237, 230], [1178, 230], [1146, 226], [1113, 221], [1073, 221], [1031, 221], [987, 218], [951, 215], [916, 215], [883, 222], [865, 229], [827, 246], [796, 259], [771, 271], [747, 285], [724, 300], [683, 301], [668, 301], [643, 305], [605, 308], [560, 312], [522, 309], [488, 309], [447, 307], [407, 307], [387, 305], [362, 304], [323, 302], [292, 303], [244, 303], [212, 304], [187, 304], [149, 304], [104, 301], [91, 299], [72, 297], [33, 297], [33, 297], [19, 280], [10, 273], [10, 246], [10, 227], [10, 193], [9, 163], [3, 140], [0, 102], [0, 76], [2, 57], [7, 45], [7, 35], [21, 27]])

# new_points = cv2.transform(points[:-20, :].reshape(1, -1, 2), M)

# cv2.fillPoly(temp, [points], color=(255,255,255))

# template_moments = cv2.HuMoments(cv2.moments(points)).flatten()
# object_moments = cv2.HuMoments(cv2.moments(new_points)).flatten()
# score = np.sqrt(np.sum((template_moments - object_moments)**2))
# print(score)

# plt.imshow(temp)
# plt.show()