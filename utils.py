import cv2
import numpy as np

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

def singleScaleRetinex(img, log_img, sigma):
    retinex = log_img - cv2.GaussianBlur(log_img, (0, 0), sigma)
    return retinex

def multiScaleRetinex(img, sigma_list):
    log_img = np.log10(img)
    kernel_sizes = [int(3 * sigma) | 1 for sigma in sigma_list]
    blurred_imgs = [cv2.GaussianBlur(log_img, (kernel_size, kernel_size), sigma) for sigma, kernel_size in zip(sigma_list, kernel_sizes)]
    retinex = np.sum([log_img - blurred_img for blurred_img in blurred_imgs], axis=0)
    retinex = retinex / len(sigma_list)
    return retinex

def colorRestoration(img, alpha, beta):
    img_sum = np.sum(img, axis=-1, keepdims=True)
    img_sum[img_sum == 0] = 1
    color_restoration = beta * (np.log10(alpha * img) - np.log10(img_sum))
    return color_restoration

def simplestColorBalance(img, low_clip, high_clip):
    low_val, high_val = np.percentile(img, (low_clip, high_clip))
    out_img = np.uint8(np.clip((img - low_val) * 255.0 / (high_val - low_val), 0, 255))
    return out_img

def MSRCP(img, sigma_list, G, b, alpha, beta, low_clip, high_clip):
    img = np.float32(img) + 1.0
    img_retinex = multiScaleRetinex(img, sigma_list)
    img_color_restoration = colorRestoration(img, alpha, beta)
    img_msrcp = G * (img_retinex * img_color_restoration + b)
    img_msrcp = (img_msrcp - np.amin(img_msrcp)) / (np.amax(img_msrcp) - np.amin(img_msrcp)) * 255
    img_msrcp = np.uint8(img_msrcp)
    img_msrcp = simplestColorBalance(img_msrcp, low_clip, high_clip)
    return img_msrcp