import numpy as np

def non_max_suppression_fast(points, overlapThresh):
    points = np.array(points)
    if points.dtype.kind == "i":
        points = points.astype("float")

    pick = []

    x1 = points[:, 0]
    y1 = points[:, 1]
    x2 = points[:, 0] + points[:, 5]
    y2 = points[:, 1] + points[:, 6]

    score = points[:, 4]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(score)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        
        overlap = (w * h) / area[idxs[:last]]
        idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
        
    return points[pick]