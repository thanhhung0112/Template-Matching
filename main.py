from Utils import *
from Component import *

from time import time
import argparse
import os
from ultralytics import YOLO

descStr = 'computer vision unit'
parser = argparse.ArgumentParser(description=descStr)
parser.add_argument('--img_path', dest='img_path', required=True)
parser.add_argument('--template_path', dest='template_path', required=True)
parser.add_argument('--threshold', dest='threshold', required=True, type=float)
parser.add_argument('--overlap', dest='overlap', default=0.4, type=float)
parser.add_argument('--method', dest='method', required=True)
parser.add_argument('--min_modify', dest='min_modify', default='-1', type=int)
parser.add_argument('--max_modify', dest='max_modify', default='1', type=int)
parser.add_argument('--enhance', dest='custom_enhance_algorithms_path', required=False)
parser.add_argument('--representation', dest='custom_representation', required=True)

args = parser.parse_args()
img_path = args.img_path
template_path = args.template_path 
threshold = args.threshold
overlap = args.overlap
method = args.method
min_modify = args.min_modify
max_modify = args.max_modify
modify_angle = np.arange(min_modify, max_modify, 1)
custom_enhance_algorithms_path = args.custom_enhance_algorithms_path
custom_representation = args.custom_representation

# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

model = YOLO('Weights/last.pt')

img = cv2.imread(img_path, 1)
template = cv2.imread(template_path, 1)

with open(custom_representation, 'r') as file:
    representation_algorithms = json.load(file)

template_gray = image_representation(template, target='template', representation_algorithms=representation_algorithms)

start = time()

with open(custom_enhance_algorithms_path, 'r') as file:
        enhance_algorithms = json.load(file)
boxes = proposal_roi(img, template, model, 0.25, enhance_algorithms=enhance_algorithms)

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

if os.path.isfile('Output/output.jpg') == True:
    os.remove('Output/output.jpg')
if os.path.isfile('Output/result.csv') == True:
    os.remove('Output/result.csv')

copy_of_good_points = deepcopy(good_points)

realistic_points = convert_position(copy_of_good_points, pixel_ratio=0.05)

export_csv(realistic_points, 'Output')

print(f'found {len(good_points)} objects')
print(f'time proposal: {time_proposal}')
print(f'time match: {end-start}')

for point_info in good_points:
    point = point_info[0], point_info[1]
    angle = point_info[2]
    width = point_info[5]
    height = point_info[6]
    
    center_x = int(point[0]+width/2)
    center_y = int(point[1]+height/2)
    
    axis_length = 100
    
    angle_rad = np.radians(angle)
    
    # Calculate the endpoint coordinates for the x-axis line
    x1 = center_x
    y1 = center_y
    x2 = int(center_x + axis_length * np.cos(angle_rad))
    y2 = int(center_y + axis_length * np.sin(angle_rad))

    # Calculate the endpoint coordinates for the y-axis line
    x3 = center_x
    y3 = center_y
    x4 = int(center_x + axis_length * np.sin(angle_rad))
    y4 = int(center_y - axis_length * np.cos(angle_rad))
    
    color_x = (0, 255, 0)
    color_y = (0, 0, 255)
    thickness = 3
    
    # Draw the x-axis line
    cv2.line(img, (x1, y1), (x2, y2), color_x, thickness)

    # Draw the y-axis line
    cv2.line(img, (x3, y3), (x4, y4), color_y, thickness)

    # cv2.circle(img, (int(point[0]+width/2), int(point[1]+height/2)), 3, (0, 0, 255), 7)
    # cv2.rectangle(img, (int(point[0]), int(point[1])), (int(point[0]+width), int(point[1]+height)), (0, 255, 0), 3)

cv2.line(img, (0, img.shape[0]), (axis_length, img.shape[0]), color_x, thickness)
cv2.line(img, (0, img.shape[0]), (0, img.shape[0]-axis_length), color_y, thickness)

if not os.path.exists("Output"):
    os.makedirs("Output")
cv2.imwrite('Output/output.jpg', img)