from Utils import *
from API import *
from Component import *

from time import time

def get_padded_image(img_gray, box, epsilon_w, epsilon_h):
    x_start, x_end = box[0] - epsilon_w, box[0] + box[2] + epsilon_w
    y_start, y_end = box[1] - epsilon_h, box[1] + box[3] + epsilon_h

    top = min(y_start, 0)
    left = min(x_start, 0)
    bottom = min(img_gray.shape[0] - y_end, 0)
    right = min(img_gray.shape[1] - x_end, 0)
    img_padded = cv2.copyMakeBorder(img_gray, abs(top), abs(bottom), abs(left), abs(right), cv2.BORDER_CONSTANT, value=0)

    return img_padded, x_start, x_end, y_start, y_end, top, left, bottom, right

def process_roi(img_padded, template_gray, method, sub_angle, threshold,
                box, epsilon_w, epsilon_h,
                top, left, bottom, right,
                x_start, x_end, y_start, y_end,
                w_temp, h_temp):
    
    roi = img_padded[y_start + abs(top):y_end + abs(top) + abs(bottom),
                     x_start + abs(left):x_end + abs(left) + abs(right)]

    if roi.shape[0] * roi.shape[1] > w_temp * h_temp * 5:
        return None

    try:
        point = match_template(roi, template_gray, method, sub_angle, 100, threshold)
    except:
        return None

    if point is None:
        return None

    point[0], point[1] = point[0] + box[0] - epsilon_w, point[1] + box[1] - epsilon_h
    if (point[0] < 0):
        point[5] = point[5] - abs(point[0])
        point[0] = 0
    if (point[1] < 0):
        point[6] = point[6] - abs(point[1])
        point[1] = 0

    return point


@app.route('/my_cvu_api', methods=['POST', 'GET'])
@cross_origin(origin='*')
def pattern_matching():
    start = time()
    if request.method == 'POST':
        api_folder = request.form.get('api_folder')
        api_folder = api_folder.replace('\\', '/')

        if platform == "linux" or platform == "linux2":
            if api_folder.startswith('//wsl.localhost/'):
                idx = api_folder.index('/home')
                api_folder = api_folder[idx:]

            if api_folder[1] == ':':
                api_folder = os.popen('wslpath "{}"'.format(api_folder)).read().strip()

        elif platform == "win32":
            api_folder = api_folder.replace('/', '\\')

        if api_folder is not None:
            os.chdir(api_folder)

        output_folder = request.form.get('output_folder')
        path_to_save_image = os.path.join(output_folder, 'output.jpg')
        path_to_save_csv = os.path.join(output_folder, 'result.csv')

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        else:
            if os.path.isfile(path_to_save_image) == True:
                os.remove(path_to_save_image)
            if os.path.isfile(path_to_save_csv) == True:
                os.remove(path_to_save_csv)

        try:
            img_path = request.form.get('img_path')
            img_path = img_path.replace('\\', '/')
            bgr_img = cv2.imread(img_path)

            template_path = request.form.get('template_path')
            template_path = template_path.replace('\\', '/')
            bgr_template = cv2.imread(template_path)

            if (bgr_img is None) or (bgr_template is None):
                return "No image founded\n"

        except FileNotFoundError:
            return "Invalid image paths\n"

        enhance_path = request.form.get('enhance')
        with open(enhance_path, 'r') as f:
            enhance_algorithms = json.load(f)
        
        representation_path = request.form.get('representation')
        with open(representation_path, 'r') as f:
            representation_algorithms = json.load(f)

        try:
            threshold = float(request.form.get('threshold'))
            overlap = float(request.form.get('overlap'))
            min_modify = int(request.form.get('min_modify'))
            max_modify = int(request.form.get('max_modify'))

        except ValueError:
            return "Invalid input values\n"

        method = request.form.get('method')
        
        modify_angle = np.arange(min_modify, max_modify, 1)

        template_gray = image_representation(bgr_template, target='template', representation_algorithms=representation_algorithms)

        boxes = proposal_roi(bgr_img, bgr_template, model, conf=0.25, enhance_algorithms=enhance_algorithms)

        img_gray = image_representation(bgr_img, target='target_image', representation_algorithms=representation_algorithms)

        good_points = []

        for box, angle in boxes:
            for next_angle in angle:
                sub_angles = next_angle + modify_angle
                
                for sub_angle in sub_angles:
                    _, _, w_temp, h_temp = rotate_template(template_gray, sub_angle)
                    epsilon_w, epsilon_h = np.abs([box[2] - w_temp, box[3] - h_temp])

                    img_padded, x_start, x_end, y_start, y_end, top, left, bottom, right = get_padded_image(img_gray, box, epsilon_w, epsilon_h)

                    point = process_roi(img_padded, template_gray, method, sub_angle, threshold,
                                        box, epsilon_w, epsilon_h, 
                                        top, left, bottom, right, 
                                        x_start, x_end, y_start, y_end, 
                                        w_temp, h_temp)

                    if point is not None:
                        good_points.append(point)

        try:
            good_points = non_max_suppression_fast(good_points, overlap)
        except:
            return 'No detection found'

        if len(good_points) == 0:
            return 'No detection found'
        
        copy_of_good_points = deepcopy(good_points)

        realistic_points = convert_position(copy_of_good_points, pixel_ratio=0.01)
        
        send_data(realistic_points, '127.0.0.1', 5003)
        
        export_csv(realistic_points, output_folder)

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
            cv2.line(bgr_img, (x1, y1), (x2, y2), color_x, thickness)

            # Draw the y-axis line
            cv2.line(bgr_img, (x3, y3), (x4, y4), color_y, thickness)

        cv2.line(bgr_img, (0, bgr_img.shape[0]), (axis_length, bgr_img.shape[0]), color_x, thickness)
        cv2.line(bgr_img, (0, bgr_img.shape[0]), (0, bgr_img.shape[0]-axis_length), color_y, thickness)
        
        cv2.imwrite(path_to_save_image, bgr_img)
        
        end = time()
        print(f'Elapsed time: {end-start}')

        return 'Done\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)