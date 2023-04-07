import cv2
import numpy as np
import matplotlib.pyplot as plt
from rotate_template import rotate_template

def gamma_correction(img, gamma):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)

def pixel_duplicate(img, ratio):
    img_float = np.array(img, np.float16)
    img_add = img + ratio*img_float
    img_add = np.clip(img_add, 0, 255)
    img_add = np.array(img_add, np.uint8)
    return img_add

def remove_shadow(img):
    dilated_img = cv2.dilate(img, np.ones((8, 8), np.uint8)) 
    bg_img = cv2.GaussianBlur(dilated_img, (15, 15), -1)
    # bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(img, bg_img)
    norm_img = diff_img.copy()
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img, 225, 255, cv2.THRESH_BINARY_INV)
    cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    return thr_img

def sharpen(img):
    img = img.astype(np.float32)
    kernel_sharpen = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
    
    img = cv2.filter2D(img, -1, kernel_sharpen)
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)

def filter_clahe(image, cliplimit=3, titleGridSize=8):
    clahe = cv2.createCLAHE(clipLimit=cliplimit, tileGridSize=(titleGridSize, titleGridSize))
    image = clahe.apply(image)
    return image

def laplacian_detect(img, ksize=3):
    dst = cv2.Laplacian(img, cv2.CV_16S, ksize=ksize)
    abs_dst = cv2.convertScaleAbs(dst)
    return abs_dst

def proposal_roi(image, template, gamma=2, cliplimit=3, titleGridSize=5, laplacian=True, ksize_edge_detection=3):
    if len(image.shape) == 3:
        new_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(template.shape) == 3:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    area_template = template.shape[0] * template.shape[1]
    
    new_image = gamma_correction(new_image, gamma=gamma)
    new_image = remove_shadow(new_image)
    new_image = filter_clahe(new_image, cliplimit=cliplimit, titleGridSize=titleGridSize)
    new_image = sharpen(new_image)

    if laplacian == True:
        new_image = laplacian_detect(new_image, ksize=ksize_edge_detection)

    # plt.imshow(new_image)
    # plt.show()

    contours, _ = cv2.findContours(new_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours = list(map(lambda x: cv2.convexHull(x, True), contours))

    # epsilon = list(map(lambda x: 0.01*cv2.arcLength(x, True), contours))
    # contours = list(map(lambda x, y: cv2.approxPolyDP(x, y, True), contours, epsilon))

    good_contours = [contours[i] for i in range(len(contours)) if (cv2.contourArea(contours[i]) > area_template/4) and (cv2.contourArea(contours[i]) < area_template)]

    # cv2.drawContours(image, good_contours, -1, (0, 255, 0), 2)
    # plt.imshow(image)
    # plt.show()

    box_anno = []
    for cnt in good_contours:
        rect = cv2.boundingRect(cnt)

        ellipse_info = cv2.fitEllipse(cnt)
        if 1 - ellipse_info[1][0] / ellipse_info[1][1] < 0.001:
            box_anno.append((*rect, (270+cv2.fitEllipse(cnt)[2], 90+cv2.fitEllipse(cnt)[2], 0)))

        angle1, angle2 = 270+cv2.fitEllipse(cnt)[2], 90+cv2.fitEllipse(cnt)[2]

        box_anno.append((*rect, (angle1, angle2)))

    return box_anno

if __name__ == '__main__':
    # img_path = 'Dataset/Src10.bmp'
    # template_path = 'Dataset/Dst10.jpg'
    # img_path = 'Dataset/Src5-135.bmp'
    # template_path = 'Dataset/Dst5.bmp'
    img_path = 'Dataset/Src2.bmp'
    template_path = 'Dataset/Dst2.bmp'

    img = cv2.imread(img_path, 1)
    template = cv2.imread(template_path, 1)

    boxes = proposal_roi(img, 
                        template,
                        gamma=2, 
                        cliplimit=3, 
                        titleGridSize=5, 
                        laplacian=True, 
                        ksize_edge_detection=5)

    for idx, (x, y, w, h, angle) in enumerate(boxes):
        cv2.rectangle(img, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 3)

    plt.imshow(img)
    plt.show()