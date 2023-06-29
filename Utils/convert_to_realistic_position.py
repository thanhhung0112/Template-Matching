import numpy as np
from Utils.calibration import *

def convert_position(points, transformation_matrix=None):
    calib = Calibration()
    
    box = np.vstack(np.array(points[:, 0]))
    center = np.vstack(np.array(points[:, 1]))
    possible_grasp_ratio = np.vstack(np.array(points[:, 2])).flatten()
    
    center_point_robot = calib.predict(center, transformation_matrix)
    center_x, center_y = center_point_robot[:, 0], center_point_robot[:, 1]
    
    angle = -box[:, 2] - 180
    angle = np.where(angle > 180, angle-360, angle)
    angle = np.where(angle < -180, angle+360, angle)
    
    score = box[:, 4] * 100
    
    center_z = np.full((center_x.shape[0]), 97)
    
    realistic_points = np.array(list(zip(center_x, center_y, center_z, angle, possible_grasp_ratio, score)), dtype=np.float32)
    
    return realistic_points