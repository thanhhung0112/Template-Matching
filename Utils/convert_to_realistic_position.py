import numpy as np

def convert_position(points, pixel_ratio):
    
    points[:, 0] = points[:, 0] * pixel_ratio
    points[:, 1] = points[:, 1] * pixel_ratio
    
    points[:, 5], points[:, 6] = points[:, 5] * pixel_ratio, points[:, 6] * pixel_ratio
    
    center_x = points[:, 0] + points[:, 5]/2
    center_y = points[:, 1] + points[:, 6]/2
    angle = points[:, 2]
    score = points[:, 4] * 100
    
    realistic_points = np.array(list(zip(center_x, center_y, angle, score)))
    
    return realistic_points