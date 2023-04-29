import cv2

def scale_template(template, percent_scale, img_max_wh):
    max_height, max_width = img_max_wh
    max_percent_height = max_height / template.shape[0] * 100
    max_percent_width = max_width / template.shape[1] * 100

    max_percent = 0
    if max_percent_width < max_percent_height:
        max_percent = max_percent_width
    else:
        max_percent = max_percent_height
    
    if percent_scale > max_percent:
        percent_scale = max_percent

    new_width = int(template.shape[1] * percent_scale / 100)
    new_height = int(template.shape[0] * percent_scale / 100)

    result = cv2.resize(template, (new_width, new_height), interpolation = cv2.INTER_AREA)

    return result, percent_scale