curl -X POST -H "Content-Type: multipart/form-data" \
			 -F "api_folder=/home/kratosth/code/Template-Matching" \
			 -F "output_folder=Output" \
			 -F "img_path=Dataset/test_custom_crop.png" \
			 -F "template_path=Template/template.jpg" \
			 -F "threshold=0.75" \
			 -F "overlap=0.4" \
			 -F "method=cv2.TM_CCORR_NORMED" \
			 -F "min_modify=-5" \
			 -F "max_modify=5" \
			 -F "enhance=Custom_enhance/Src1-2.json" \
			 -F "representation=Custom_representation/Src-all.json" \
			 http://127.0.0.1:5000/my_cvu_api

# 'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
# 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'