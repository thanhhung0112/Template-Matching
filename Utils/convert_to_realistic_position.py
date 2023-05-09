def convert_position(points, pixel_ratio):
    
    points[:, 0] = points[:, 0] * pixel_ratio
    points[:, 1] = points[:, 1] * pixel_ratio
    
    points[:, 5], points[:, 6] = points[:, 5] * pixel_ratio, points[:, 6] * pixel_ratio
    
    
    return points