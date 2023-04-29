import requests
import cv2
import numpy as np

from API import *

@app.route('/my_camera_api', methods=['POST', 'GET'])
@cross_origin(origin='*')
def get_frame():
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

        ip_address = request.form.get('ip_address')
        ip_address = f'http://{ip_address}:8080/shot.jpg'

        img_resp = requests.get(ip_address)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        path_to_save_image = os.path.join(output_folder, 'input_image.png')
        if os.path.isfile(path_to_save_image) == True:
            os.remove(path_to_save_image)

        cv2.imwrite(path_to_save_image, img)
        
        return "Done"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)



    