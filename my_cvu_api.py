from flask import Flask, request
from flask_cors import CORS, cross_origin

import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from utils import *
from proposal_box_improve import proposal_roi
from match_template import match_template
from non_max_suppression import non_max_suppression_fast
from rotate_template import rotate_template
from image_representation import image_representation
from time import time
import json
from export_csv import export_csv
import os
from sys import platform

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['POST', 'GET'])
@cross_origin(origin='*')
def pattern_matching():
    if request.method == 'POST':
        img = Image.open(request.files['img']).convert('RGB')
        img = np.array(img)

        template = Image.open(request.files['template']).convert('RGB')
        template = np.array(template)

        bgr_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        bgr_template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)

        threshold = float(request.form.get('threshold'))
        overlap = float(request.form.get('overlap'))
        method = request.form.get('method')
        min_modify = int(request.form.get('min_modify'))
        max_modify = int(request.form.get('max_modify'))
        modify_angle = np.arange(min_modify, max_modify, 1)

        enhance_algorithms = request.files['enhance']
        enhance_algorithms = json.load(enhance_algorithms)

        representation_algorithms = request.files['representation']
        representation_algorithms = json.load(representation_algorithms)

        output_folder = request.form.get('output_folder')
        output_folder = output_folder.replace('\\', '/')
        
        if platform == "linux" or platform == "linux2":
            if output_folder.startswith('//wsl.localhost/'):
                idx = output_folder.index('/home')
                output_folder = output_folder[idx:]

            if output_folder[1] == ':':
                output_folder = os.popen('wslpath "{}"'.format(output_folder)).read().strip()

        elif platform == "win32":
            output_folder = output_folder.replace('/', '\\')

        template_gray = image_representation(bgr_template, target='template', representation_algorithms=representation_algorithms)

        boxes, _ = proposal_roi(bgr_img, template, enhance_algorithms=enhance_algorithms)

        img_gray = image_representation(bgr_img, target='target_image', representation_algorithms=representation_algorithms)

        print(boxes)

        good_points = []
        for box, angle in boxes:
            for next_angle in angle:
                sub_angles = next_angle + modify_angle
                for sub_angle in sub_angles:
                    _, _, w_temp, h_temp = rotate_template(template_gray, sub_angle)
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

                    if roi.shape[0]*roi.shape[1] > w_temp*h_temp*5:
                        continue

                    try:
                        point = match_template(roi, template_gray, method, sub_angle, 100, threshold)
                        # print(f'Point: {point}')
                    except:
                        continue

                    if point is None:
                        continue

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

        if len(good_points) == 0:
            return 'No detection found'

        path_to_save_image = os.path.join(output_folder, 'output.jpg')
        path_to_save_csv = os.path.join(output_folder, 'result.csv')

        if os.path.isfile(path_to_save_image) == True:
            os.remove(path_to_save_image)
        if os.path.isfile(path_to_save_csv) == True:
            os.remove(path_to_save_csv)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        export_csv(good_points, output_folder)

        for point_info in good_points:
            point = point_info[0], point_info[1]
            width = point_info[5]
            height = point_info[6]

            cv2.circle(img, (int(point[0]+width/2), int(point[1]+height/2)), 3, (0, 0, 255), 7)
            cv2.rectangle(img, (int(point[0]), int(point[1])), (int(point[0]+width), int(point[1]+height)), (0, 255, 0), 3)

        cv2.imwrite(path_to_save_image, img)

        return 'Done'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
