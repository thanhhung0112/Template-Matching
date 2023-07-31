from Utils import *
from API import *
from Component import *

from time import time

logger = logging.getLogger(__name__)

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
                top, left, bottom, right,
                x_start, x_end, y_start, y_end):
    
    roi = img_padded[y_start + abs(top):y_end + abs(top) + abs(bottom),
                    x_start + abs(left):x_end + abs(left) + abs(right)]

    try:
        point = match_template(roi, template_gray, method, sub_angle, 100, threshold)
    except Exception as e:
        logger.error(f'{e}\n')
        return None

    return point

def match_pattern(img_gray, template_gray, box, sub_angle, method, threshold):
    _, _, w_temp, h_temp = rotate_template(template_gray, sub_angle)
    epsilon_w, epsilon_h = np.abs([box[2] - w_temp, box[3] - h_temp])

    img_padded, x_start, x_end, y_start, y_end, top, left, bottom, right = get_padded_image(img_gray, box, epsilon_w, epsilon_h)

    point = process_roi(img_padded, template_gray, method, sub_angle, threshold,
                        top, left, bottom, right, 
                        x_start, x_end, y_start, y_end)
    
    return point


@app.route('/my_cvu_api', methods=['POST', 'GET'])
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
        
        if not os.path.exists('Log'):
            os.makedirs('Log')
        
        logging.basicConfig(level=logging.INFO, 
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S', 
                    filename='Log/log.txt',
                    filemode='w')
        
        logger.info(f'OS: {platform}\n')
        logger.info(f'Root folder: {api_folder}\n')

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
                
        logger.info(f'Output folder: {output_folder}\n')

        try:
            img_path = request.form.get('img_path')
            img_path = img_path.replace('\\', '/')
            bgr_img, _ = loader.load(img_path)

            template_path = request.form.get('template_path')
            template_path = template_path.replace('\\', '/')
            bgr_template, _ = loader.load(template_path)

            if (bgr_img is None) or (bgr_template is None):
                logger.warning("No image founded\n")
                return f'{0}'

        except Exception as e:
            logger.error(f'{e}\n')
            return f'{0}'
        
        logger.info('Load images successfully\n')
        
        try:
            threshold = float(request.form.get('threshold'))
            overlap = float(request.form.get('overlap'))
            min_modify = int(request.form.get('min_modify'))
            max_modify = int(request.form.get('max_modify'))
            conf_score = float(request.form.get('conf_score'))
            img_size = int(request.form.get('img_size'))
            server_ip = request.form.get('server_ip')

        except Exception as e:
            logger.error(f'{e}\n')
            return f'{0}'

        method = request.form.get('method')
        
        logger.info(f'''
                    threshold: {threshold}
                    overlap: {overlap}
                    min_modify: {min_modify}
                    max_modify: {max_modify}
                    conf_score: {conf_score}
                    method: {method}
                    img_size: {img_size}
                    server_ip: {server_ip}\n
                    ''')
        
        minus_modify_angle = np.arange(-1, min_modify, -1)
        plus_modify_angle = np.arange(1, max_modify, 1)

        template_gray = cv2.cvtColor(bgr_template, cv2.COLOR_BGR2GRAY)
        
        copy_of_template_gray = deepcopy(template_gray)
        copy_of_template_gray = contrast_stretching(copy_of_template_gray, {"low_clip": 10, "high_clip": 90})
        _, copy_of_template_gray = cv2.threshold(copy_of_template_gray, 100, 255, cv2.THRESH_BINARY_INV)
        cv2.imwrite('intensity_template.jpg', copy_of_template_gray)
        
        intensity_of_template_gray = np.sum(copy_of_template_gray == 0)

        try:
            s = time()
            boxes = proposal_box_yolo(bgr_img, model, conf_score=conf_score, img_size=img_size)
            e = time()
            print(f'time: {e-s}')
        except Exception as e:
            logger.error(f'{e}\n')
            return f'{0}'
            
        logger.info(f'''
                    Number of proposal boxes: {len(boxes)}\n
                    {np.array(boxes, dtype=object)}\n
                    ''')

        img_gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
        
        copy_of_img_gray = deepcopy(img_gray)

        s = time()
        good_points = []
        for box, angle in boxes:
            center_obj, possible_grasp_ratio = find_center(copy_of_img_gray, box, intensity_of_template_gray)
            if possible_grasp_ratio < 40:
                continue
            
            minus_sub_angles = angle + minus_modify_angle
            plus_sub_angles = angle + plus_modify_angle
            minus_length = len(minus_sub_angles)
            plus_length = len(plus_sub_angles)
            
            minus_pointer, minus_check = 0, False
            plus_pointer, plus_check = 0, False
            sub_minus_points = []
            sub_plus_points = []
            
            point = match_pattern(img_gray, template_gray, box, angle, method, threshold)
            if point is None:
                continue
            
            while True:
                if (minus_length == 0 and plus_length == 0):
                    break

                if minus_length == 0 or minus_pointer >= minus_length:
                    minus_check = True
                elif plus_length == 0 or plus_pointer >= plus_length:
                    plus_check = True

                if not minus_check and minus_length != 0:
                    minus_point = match_pattern(img_gray, template_gray, box, minus_sub_angles[minus_pointer], method, threshold)
                    if minus_point is not None:
                        minus_check = minus_point[4] < point[4] if minus_pointer == 0 else minus_point[4] < sub_minus_points[-1][4]
                    else:
                        minus_check = True
                    
                    if not minus_check:
                        sub_minus_points.append(minus_point)
                        minus_pointer += 1
                
                if not plus_check and plus_length != 0:
                    plus_point = match_pattern(img_gray, template_gray, box, plus_sub_angles[plus_pointer], method, threshold)
                    if plus_point is not None:
                        plus_check = plus_point[4] < point[4] if plus_pointer == 0 else plus_point[4] < sub_plus_points[-1][4]
                    else:
                        plus_check = True
                    
                    if not plus_check:
                        sub_plus_points.append(plus_point)
                        plus_pointer += 1
                
                if minus_check and plus_check:
                    break
            
            best_minus_point = sub_minus_points[-1] if sub_minus_points else None
            best_plus_point = sub_plus_points[-1] if sub_plus_points else None
            
            if (best_minus_point is not None) and (best_plus_point is not None):
                best_point = best_minus_point if best_minus_point[4] > best_plus_point[4] else best_plus_point
            elif (best_minus_point is None) and (best_plus_point is None):
                best_point = point
            else:
                best_point = best_minus_point or best_plus_point
            
            if point:
                good_points.append((best_point, center_obj, possible_grasp_ratio))
        
        good_points.sort(key=lambda x: x[2], reverse=True)
        good_points = np.array(good_points, dtype=object)
        e = time()
        print(f'time: {e-s}')
        
        if len(good_points) == 0:
            logger.warning('No detection found\n')
            return f'{0}'
        
        copy_of_good_points = deepcopy(good_points)

        realistic_points = convert_position(copy_of_good_points, transformation_matrix)
        
        logger.info(f'Result: \n{realistic_points}\n')
        
        s = time()
        send_float_array_data(realistic_points[:, :4], server_ip, 48952)
        e = time()
        print(f'time: {e-s}')
        
        export_csv(realistic_points, output_folder)
        
        for idx, (point_info, center, possible_grasp_ratio) in enumerate(good_points):
            angle = point_info[2]
            
            center_x, center_y = center
            center_x, center_y = int(center_x), int(center_y)
            
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
            
            cv2.putText(bgr_img, str(idx), (center_x+50, center_y+50), cv2.FONT_HERSHEY_SIMPLEX, 3, color_x, thickness)

        cv2.line(bgr_img, (0, bgr_img.shape[0]), (axis_length, bgr_img.shape[0]), color_x, thickness)
        cv2.line(bgr_img, (0, bgr_img.shape[0]), (0, bgr_img.shape[0]-axis_length), color_y, thickness)
        
        bgr_img = cv2.resize(bgr_img, (bgr_img.shape[1]//1, bgr_img.shape[0]//1))
        
        cv2.imwrite(path_to_save_image, bgr_img, [cv2.IMWRITE_JPEG_QUALITY, 70])
        
        end = time()
        print(f'Elapsed time: {end-start}\n')
        logger.info(f'Elapsed time: {end-start}\n')

        return f'{len(realistic_points)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)