
## Introduction
This repository aims to detect multi same objects in one image for grasping robot
## Getting Started
Clone this repository and install all dependencies
```bash
git clone https://github.com/thanhhung0112/Template-Matching.git
cd Template-Matching
pip install -r requirements.txt
```

## Usage
Running the command line
```bash
python main.py --img_path <path/to/the/image> \
               --template_path <path/to/the/template> \
               --threshold <the similarity score> \
               --overlap <the ratio to remove redundant box> \
               --method <the method to compute similarity in opencv> \
               --min_modify -1 \
               --max_modify 1 \
               --enhance <path/to/the/enhance/algorithms/json/file> \
               --representation <path/to/the/representation/algorithms/json/file>
```
The result will be saved in `Output` folder including `output.jpg` file which visualizes the boxes and centers of objects inside and `result.csv` file which saves all the pixel center positions, angles and scores of objects inside

Running the following command line if you would like to use api endpoint instead
```bash
python my_cvu_api.py
```

You have to send the `Post` request with key-value pairs to the api endpoint

```bash
curl -X POST -H "Content-Type: multipart/form-data" \
			 -F "api_folder=<path/to/the/folder/which/api/will/run/in/this>" \
			 -F "output_folder=<path/to/output/folder/you/want/to/save>" \
			 -F "img_path=<relative/path/to/the/image>" \
			 -F "template_path=<relative/path/to/the/template>" \
			 -F "threshold=0.75" \
			 -F "overlap=0.4" \
			 -F "method=cv2.TM_CCOEFF_NORMED" \
			 -F "min_modify=-1" \
			 -F "max_modify=1" \
			 -F "enhance=<relative/path/to/the/enhance/json/file>" \
			 -F "representation=<relative/path/to/the/representation/json/file>" \
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
			 -F "enhance=Custom_enhance/Src1-2.json" \
			 -F "representation=Custom_representation/Src1-2.json" \
			 http://127.0.0.1:5000/my_cvu_api
```