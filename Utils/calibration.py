import numpy as np
import os

class Calibration:
    def __init__(self):
        ...
    
    @staticmethod
    def calibrate_homography(input_points, output_points, predict_points=ModuleNotFoundError):
        # Add homogeneous coordinate 1 to each input point
        input_points_homogeneous = np.hstack((input_points, np.ones((input_points.shape[0], 1))))
        # Solve for the transformation matrix
        transformation_matrix, _ = np.linalg.lstsq(input_points_homogeneous, output_points, rcond=None)[:2]
        # Convert the transformation matrix to a 3x3 matrix
        transformation_matrix = np.vstack((transformation_matrix.T, [0, 0, 1]))
        
        if predict_points is not None:
            new_input_points = np.array(predict_points)
            new_input_points_homogeneous = np.hstack((new_input_points, np.ones((new_input_points.shape[0], 1))))
            output_points = np.dot(transformation_matrix, new_input_points_homogeneous.T).T
            return transformation_matrix, output_points
        
        return transformation_matrix
    
    @staticmethod
    def save_transformation_matrix(transformation_matrix, calib_path):
        if not os.path.exists(calib_path):
            os.makedirs(calib_path)
            
        transformation_matrix_path = os.path.join(calib_path, "transformation_matrix.npy")
        np.save(transformation_matrix_path, transformation_matrix)
        
    @staticmethod
    def predict(center_obj, transformation_matrix_path):
        transformation_matrix = np.load(transformation_matrix_path)
        
        center_points = np.array(center_obj)
        center_points = np.hstack((center_points, np.ones((center_points.shape[0], 1))))
        robot_points = np.dot(transformation_matrix, center_points.T).T
        
        center_point_robot = robot_points[:, :2]
        return center_point_robot
    
    
if __name__ == '__main__':
    calib = Calibration()
    transformation_matrix = calib.calibrate_homography()
    calib.save_transformation_matrix(transformation_matrix)