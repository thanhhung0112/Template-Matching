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
    except Exception as e:
        logger.error(f'{e}\n')
        return None

    # if point is None:
    #     return None

    # point[0], point[1] = point[0] + box[0] - epsilon_w, point[1] + box[1] - epsilon_h
    # if (point[0] < 0):
    #     point[5] = point[5] - abs(point[0])
    #     point[0] = 0
    # if (point[1] < 0):
    #     point[6] = point[6] - abs(point[1])
    #     point[1] = 0

    return point

def match_pattern(img_gray, template_gray, box, sub_angle, method, threshold):
    _, _, w_temp, h_temp = rotate_template(template_gray, sub_angle)
    epsilon_w, epsilon_h = np.abs([box[2] - w_temp, box[3] - h_temp])

    img_padded, x_start, x_end, y_start, y_end, top, left, bottom, right = get_padded_image(img_gray, box, epsilon_w, epsilon_h)

    point = process_roi(img_padded, template_gray, method, sub_angle, threshold,
                        box, epsilon_w, epsilon_h, 
                        top, left, bottom, right, 
                        x_start, x_end, y_start, y_end, 
                        w_temp, h_temp)
    
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
            bgr_img = cv2.imread(img_path)

            template_path = request.form.get('template_path')
            template_path = template_path.replace('\\', '/')
            bgr_template = cv2.imread(template_path)

            if (bgr_img is None) or (bgr_template is None):
                logger.warning("No image founded\n")
                return "No image founded\n"

        except Exception as e:
            logger.error(f'{e}\n')
            return f'{e}\n'
        
        logger.info('Load images successfully\n')
        
        try:
            threshold = float(request.form.get('threshold'))
            overlap = float(request.form.get('overlap'))
            min_modify = int(request.form.get('min_modify'))
            max_modify = int(request.form.get('max_modify'))
            conf_score = float(request.form.get('conf_score'))
            img_size = int(request.form.get('img_size'))
            robot_ip = request.form.get('robot_ip')

        except Exception as e:
            logger.error(f'{e}\n')
            return f'{e}\n'

        method = request.form.get('method')
        
        logger.info(f'''
                    threshold: {threshold}
                    overlap: {overlap}
                    min_modify: {min_modify}
                    max_modify: {max_modify}
                    conf_score: {conf_score}
                    method: {method}
                    img_size: {img_size}
                    robot_ip: {robot_ip}\n
                    ''')
        
        minus_modify_angle = np.arange(-1, min_modify, -1)
        plus_modify_angle = np.arange(1, max_modify, 1)

        template_gray = cv2.cvtColor(bgr_template, cv2.COLOR_BGR2GRAY)

        try:
            s = time()
            boxes = proposal_box_yolo(bgr_img, model, conf_score=conf_score, img_size=img_size)
            e = time()
            print(f'time: {e-s}')
        except Exception as e:
            logger.error(f'{e}\n')
            return f'{e}\n'
            
        logger.info(f'''
                    Number of proposal boxes: {len(boxes)}\n
                    {np.array(boxes, dtype=object)}\n
                    ''')

        img_gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

        good_points = []
        for box, angle in boxes:
            center_obj = find_center(img_gray, box, gamma=1)
            # center_obj = box[0] + box[2]//2, box[1] + box[3]//2
            
            minus_sub_angles = angle + minus_modify_angle
            plus_sub_angles = angle + plus_modify_angle
            minus_pointer, minus_check = 0, 0
            plus_pointer, plus_check = 0, 0
            sub_minus_points = []
            sub_plus_points = []
            sub_good_points = []
            
            point = match_pattern(img_gray, template_gray, box, angle, method, threshold)
            sub_good_points.append(point)
            
            while True:
                if not minus_check:
                    minus_point = match_pattern(img_gray, template_gray, box, minus_sub_angles[minus_pointer], method, threshold)
                    if minus_pointer == 0:
                        minus_check = not (minus_point[4] >= point[4])
                    else:
                        minus_check = not (minus_point[4] >= sub_minus_points[-1][4])
                        
                    if not minus_check:
                        sub_minus_points.append(minus_point)
                        minus_pointer += 1
                    
                if not plus_check:
                    plus_point = match_pattern(img_gray, template_gray, box, plus_sub_angles[plus_pointer], method, threshold)
                    if plus_pointer == 0:
                        plus_check = not (plus_point[4] >= point[4])
                    else:
                        plus_check = not (plus_point[4] >= sub_plus_points[-1][4])
                        
                    if not plus_check:
                        sub_plus_points.append(plus_point)
                        plus_pointer += 1
                        
                if (minus_check == 1) and (plus_check == 1):
                    break
            
            best_minus_point = sub_minus_points[-1] if len(sub_minus_points) else None
            best_plus_point = sub_plus_points[-1] if len(sub_plus_points) else None
            
            if (best_minus_point is not None) and (best_plus_point is not None):
                best_point = best_minus_point if best_minus_point[4] > best_plus_point[4] else best_plus_point
            elif (best_minus_point is None) and (best_plus_point is None):
                best_point = point
            else:
                best_point = best_minus_point if best_minus_point is not None else best_plus_point
                
            if point is not None:
                good_points.append((best_point, center_obj))
        
        good_points = np.array(good_points, dtype=object)
        
        # try:
        #     good_points = np.array(good_points, dtype=object)
        #     good_points = non_max_suppression_fast(good_points, overlap)
        # except:
        #     logger.warning('No detection found\n')
        #     return 'No detection found\n'
        
        if len(good_points) == 0:
            logger.warning('No detection found\n')
            return 'No detection found\n'
        
        copy_of_good_points = deepcopy(good_points)

        realistic_points = convert_position(copy_of_good_points, transformation_matrix)
        
        logger.info(f'Result: \n{realistic_points}\n')
        
        send_float_array_data(realistic_points[:, :4], robot_ip, 48952)
        
        export_csv(realistic_points, output_folder)
        
        for point_info, center in good_points:
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

        cv2.line(bgr_img, (0, bgr_img.shape[0]), (axis_length, bgr_img.shape[0]), color_x, thickness)
        cv2.line(bgr_img, (0, bgr_img.shape[0]), (0, bgr_img.shape[0]-axis_length), color_y, thickness)
        
        cv2.imwrite(path_to_save_image, bgr_img)
        
        end = time()
        logger.info(f'Elapsed time: {end-start}\n')

        return 'Done\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)