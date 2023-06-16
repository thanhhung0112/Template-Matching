import numpy as np
from Utils.calibration import *

def convert_position(points, transformation_matrix=None):
    calib = Calibration()
    
    box = np.vstack(np.array(points[:, 0]))
    center = np.vstack(np.array(points[:, 1]))
    
    center_point_robot = calib.predict(center, transformation_matrix)
    center_x, center_y = center_point_robot[:, 0], center_point_robot[:, 1]
    
    angle = -box[:, 2] - 180
    score = box[:, 4] * 100
    
    center_z = np.full((center_x.shape[0]), 97)
    
    realistic_points = np.array(list(zip(center_x, center_y, center_z, angle, score)), dtype=np.float32)
    
    return realistic_points