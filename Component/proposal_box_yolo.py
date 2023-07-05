import numpy as np
from Utils.proposal_angle import apply_min_area

class YOLOSegmentation:
    def __init__(self, model):
        self.model = model

    def predict(self, img, conf_score, img_size):
        pred_img = self.model.predict(source=img, show=False, save=True, conf=conf_score, imgsz=img_size)
        
        # get bounding boxes
        bboxes = np.array(pred_img[0].boxes.xyxy, dtype="int")
        # get masks
        masks = np.array(pred_img[0].masks.xy, dtype=object)
        # get class of bboxes
        class_ids = np.array(pred_img[0].boxes.cls, dtype="int")
        # get score of bboxes
        scores = np.array(pred_img[0].boxes.conf, dtype="float").round(2)
        
        return bboxes, class_ids, masks, scores
    
    @staticmethod
    def filter_boxes(bboxes, class_ids, masks, scores):
        obj_idx = class_ids == 0
        obj = bboxes[obj_idx, :], masks[obj_idx], scores[obj_idx]
        fail_obj = bboxes[~obj_idx, :], masks[~obj_idx], scores[~obj_idx]
        return obj, fail_obj
    
    @staticmethod
    def compute_angle(masks_obj):
        angles_pred = list(map(lambda x: apply_min_area(x), masks_obj))   
        return angles_pred
    
    @staticmethod
    def convert_boxes(boxes): # xyxy to xywh
        boxes[:, 2], boxes[:, 3] = boxes[:, 2] - boxes[:, 0], boxes[:, 3] - boxes[:, 1]
        return boxes
    
def proposal_box_yolo(img, model, conf_score, img_size):
    ys = YOLOSegmentation(model)
    
    bboxes, class_ids, masks, scores = ys.predict(img, conf_score, img_size)
    obj, _ = ys.filter_boxes(bboxes, class_ids, masks, scores)
    angles_pred = ys.compute_angle(obj[1])
    new_bboxes = ys.convert_boxes(obj[0])
    
    return list(zip(new_bboxes, angles_pred))
        
            