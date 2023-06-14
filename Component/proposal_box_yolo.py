import numpy as np
from Utils.proposal_angle import apply_min_area

class YOLOSegmentation:
    def __init__(self, model):
        self.model = model

    def predict(self, img, conf_score, img_size):
        pred_img = self.model.predict(source=img, show=False, save=True, conf=conf_score, imgsz=img_size)
        # get contour
        segmentation_contour_idx = []
        for seg in pred_img[0].masks.xy:
            segment = np.array(seg, dtype=np.int32)
            segmentation_contour_idx.append(segment)
        # get bounding boxes
        bboxes = np.array(pred_img[0].boxes.xyxy, dtype="int")
        # get class of bboxes
        class_ids = np.array(pred_img[0].boxes.cls, dtype="int")
        # get score of bboxes
        scores = np.array(pred_img[0].boxes.conf, dtype="float").round(2)
        return bboxes, class_ids, segmentation_contour_idx, scores
    
    @staticmethod
    def filter_boxes(bboxes, class_ids, masks, scores):
        bboxes_obj = [bbox for bbox, class_id in zip(bboxes, class_ids) if class_id == 0]
        masks_obj = [mask for mask, class_id in zip(masks, class_ids) if class_id == 0]
        scores_obj = [score for score, class_id in zip(scores, class_ids) if class_id == 0]

        bboxes_other_classes = [bbox for bbox, class_id in zip(bboxes, class_ids) if class_id != 0]
        masks_other_classes = [mask for mask, class_id in zip(masks, class_ids) if class_id != 0]
        scores_other_classes = [score for score, class_id in zip(scores, class_ids) if class_id != 0]
        
        return (bboxes_obj, masks_obj, scores_obj), (bboxes_other_classes, masks_other_classes, scores_other_classes)
    
    @staticmethod
    def compute_angle(masks_obj):
        angles_pred = []
        for mask in masks_obj:
            angle, _ = apply_min_area(mask)
            angles_pred.append([angle])
            
        return angles_pred
    
    @staticmethod
    def convert_boxes(boxes): # xyxy to xywh
        new_bboxes = []
        for bbox in boxes:
            (x1, y1, x2, y2) = bbox
            w = x2 - x1
            h = y2 - y1
            new_bbox = (x1, y1, w, h)
            new_bboxes.append(new_bbox)
            
        return new_bboxes
    
def proposal_box_yolo(img, model, conf_score, img_size):
    ys = YOLOSegmentation(model)
    bboxes, class_ids, masks, scores = ys.predict(img, conf_score, img_size)
    obj, _ = ys.filter_boxes(bboxes, class_ids, masks, scores)
    angles_pred = ys.compute_angle(obj[1])
    new_bboxes = ys.convert_boxes(obj[0])
    return list(zip(new_bboxes, angles_pred))
        
            