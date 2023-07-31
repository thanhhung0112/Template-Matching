## Introduction
This repository aims to detect multi same objects in one image for grasping robot using YoloV8 and some traditional techniques in computer vision via OpenCV-Python
## Getting Started
Clone this repository and install all dependencies
```bash
git clone https://github.com/thanhhung0112/Template-Matching.git
cd Template-Matching
pip install -r requirements.txt
```
## Usage
Running the following command line for using api endpoint
```bash
python my_cvu_api.py
```
You have to send the `Post` request with key-value pairs to the api endpoint
```bash
curl -X POST -H "Content-Type: multipart/form-data" \
			 -F "api_folder=<path/to/the/folder/which/api/will/run/in/this>" \
			 -F "output_folder=<relative/path/to/output/folder/you/want/to/save>" \
			 -F "img_path=<relative/path/to/the/image>" \
			 -F "template_path=<relative/path/to/the/template>" \
			 -F "threshold=0.75" \
			 -F "overlap=0.4" \
			 -F "method=cv2.TM_CCOEFF_NORMED" \
			 -F "min_modify=-1" \
			 -F "max_modify=1" \
			 -F "server_ip=<id address of your computer>"\
			 http://127.0.0.1:5000/my_cvu_api
```
Example 
```bash
curl -X POST -H "Content-Type: multipart/form-data" \
			 -F "api_folder=/home/kratos/code/Capstone/Demo-model-AI/Template-Matching" \
			 -F "output_folder=Output" 
			 -F "img_path=Dataset/Src1.bmp" \
			 -F "template_path=Dataset/20220611.bmp" \
			 -F "threshold=0.75" \
			 -F "overlap=0.4" \
			 -F "method=cv2.TM_CCOEFF_NORMED" \
			 -F "min_modify=-1" \
			 -F "max_modify=1" \
			 -F "server_ip=192.168.0.105"
			 http://127.0.0.1:5000/my_cvu_api
```
Using [Postman](https://www.postman.com/downloads/) to send the request to api endpoint instead if you do not want to use command line.
## User Interface
Using `Winforms application` to create the UI for easily program manipulating
![image](https://github.com/thanhhung0112/Template-Matching/assets/79474374/c585cd92-d6a0-4e05-acfb-12f8d77ee73b) 
You can configure params for api endpoint at `General Setting` and enter an IP address to `Server IP`
