import cv2
import numpy as np
from rembg import remove
import inspect
import matplotlib.pyplot as plt

def with_params(func):
    def wrapper(img, params):
        return func(img, **{k: params[k] for k in inspect.signature(func).parameters.keys() if k in params})
    return wrapper

@with_params
def rembg_add_weights(img, alpha=0.75, beta=2.5):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    enhanced_img = remove(img)
    enhanced_img = cv2.cvtColor(enhanced_img, cv2.COLOR_BGRA2GRAY)
    enhanced_img = cv2.addWeighted(img, alpha, enhanced_img, beta, 0)
    return enhanced_img

@with_params
def adaptive_threshold(img, iteration=1):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    score, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_TRIANGLE)
    score = int(score)
    # peak1 = np.argmax(hist.T[0][:score])
    peak2 = np.argmax(hist.T[0][score:]) + score
    
    if peak2 == 255:
        _, mask = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)
    
    else:
        _, mask = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_TRIANGLE)

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)

    return mask

def remove_wrong_contours(img, area_temp, selection_area=[0.25, 1.5]):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    _, labels, stats_img, _ = cv2.connectedComponentsWithStats(img)
    areas_img = stats_img[:, 4]

    binary = np.zeros_like(img)

    mask = (areas_img[1:] >= area_temp*selection_area[0]) & (areas_img[1:] <= area_temp*selection_area[1])
    indices = np.where(mask)[0] + 1
    binary[np.isin(labels, indices)] = 255
    return binary

@with_params
def gamma_correction(img, gamma):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)

@with_params
def pixel_duplicate(img, ratio):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    img_float = np.array(img, np.float16)
    enhanced_img = img + ratio*img_float
    enhanced_img = np.clip(enhanced_img, 0, 255)
    enhanced_img = np.array(enhanced_img, np.uint8)
    return enhanced_img

@with_params
def remove_shadow(img, blur=21, thresh=220):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    dilated_img = cv2.dilate(img, np.ones((8, 8), np.uint8)) 
    bg_img = cv2.GaussianBlur(dilated_img, (blur, blur), -1)
    diff_img = 255 - cv2.absdiff(img, bg_img)
    norm_img = diff_img.copy()
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img, thresh, 255, cv2.THRESH_BINARY_INV)
    cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    return thr_img

@with_params
def sharpen(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    img = img.astype(np.float32)
    kernel_sharpen = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
    
    img = cv2.filter2D(img, -1, kernel_sharpen)
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)

@with_params
def filter_clahe(img, cliplimit=3, titleGridSize=8):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    clahe = cv2.createCLAHE(clipLimit=cliplimit, tileGridSize=(titleGridSize, titleGridSize))
    img = clahe.apply(img)
    return img

@with_params
def laplacian_detect(img, ksize=3):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    dst = cv2.Laplacian(img, cv2.CV_16S, ksize=ksize)
    abs_dst = cv2.convertScaleAbs(dst)
    return abs_dst

@with_params
def gradient(img, ksize=3):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)
    grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=ksize)
    grad_mag = np.sqrt(grad_x ** 2 + grad_y ** 2)
    grad_mag_norm = cv2.normalize(grad_mag, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return grad_mag_norm

@with_params
def canny_detect(img, thresh1=100, thresh2=200):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    return cv2.Canny(img, thresh1, thresh2)

@with_params
def contrast_stretching(img, low_clip=5.0, high_clip=97.0):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    low_val, high_val = np.percentile(img, (low_clip, high_clip))
    out_img = np.uint8(np.clip((img - low_val) * 255.0 / (high_val - low_val), 0, 255))
    return out_img

def multiScaleRetinex(img, sigma_list=[15, 80, 256]):
    log_img = np.log10(img)
    kernel_sizes = [int(3 * sigma) | 1 for sigma in sigma_list]
    blurred_imgs = [cv2.GaussianBlur(log_img, (kernel_size, kernel_size), sigma) for sigma, kernel_size in zip(sigma_list, kernel_sizes)]
    retinex = np.sum([log_img - blurred_img for blurred_img in blurred_imgs], axis=0)
    retinex = retinex / len(sigma_list)
    return retinex

def colorRestoration(img, alpha=125, beta=50):
    img_sum = np.sum(img, axis=-1, keepdims=True)
    img_sum[img_sum == 0] = 1
    color_restoration = beta * (np.log10(alpha * img) - np.log10(img_sum))
    return color_restoration

def simplestColorBalance(img, low_clip=5.0, high_clip=97.0):
    low_val, high_val = np.percentile(img, (low_clip, high_clip))
    out_img = np.uint8(np.clip((img - low_val) * 255.0 / (high_val - low_val), 0, 255))
    return out_img

@with_params
def MSRCP(img, sigma_list=[15, 80, 256], G=5, b=25, alpha=125, beta=50, low_clip=5.0, high_clip=97.0, pyramid=2):
    assert len(img.shape) == 3, "The image has to be a color image"
    for _ in range(pyramid):
        img = cv2.pyrDown(img)

    img = np.float32(img) + 1.0
    img_retinex = multiScaleRetinex(img, sigma_list)
    img_color_restoration = colorRestoration(img, alpha, beta)
    img_msrcp = G * (img_retinex * img_color_restoration + b)
    img_msrcp = (img_msrcp - np.amin(img_msrcp)) / (np.amax(img_msrcp) - np.amin(img_msrcp)) * 255
    img_msrcp = np.uint8(img_msrcp)
    img_msrcp = simplestColorBalance(img_msrcp, low_clip, high_clip)
    img_msrcp = cv2.cvtColor(img_msrcp, cv2.COLOR_BGR2GRAY) if len(img_msrcp.shape) == 3 else img_msrcp

    for _ in range(pyramid):
        img_msrcp = cv2.pyrUp(img_msrcp)

    return img_msrcp

@with_params
def apply_representation(img, color='lab', channel=0):
    assert len(img.shape) == 3, "The image has to be a color image"
    assert channel <= 2, "The channel has to be smaller and equal 2"

    if color == 'lab':
        new_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        return new_img[:, :, channel]
    elif color == 'hsv':
        new_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return new_img[:, :, channel]
    elif color == 'gray':
        new_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return new_img
