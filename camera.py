# Import essential libraries
import requests
import cv2
import numpy as np
import argparse

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
# url = "http://192.168.1.5:8080/shot.jpg"

descStr = 'camera unit'
parser = argparse.ArgumentParser(description=descStr)
parser.add_argument('--ip', dest='ip_address', required=True)

def get_frame(url):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    cv2.imwrite('Stream_camera/input_image.png', img)

if __name__ == '__main__':
    args = parser.parse_args()
    ip_address = args.ip_address
    # ip_address = ip_address + "/shot.jpg"
    ip_address = f'http://{ip_address}:8080/shot.jpg'

    get_frame(ip_address)