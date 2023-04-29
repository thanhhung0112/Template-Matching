import numpy as np
import matplotlib.pyplot as plt
from Utils.image_processing_algorithms import *

def image_representation(img, target, representation_algorithms):
    if target == 'template':
        algorithms = representation_algorithms['template']
    elif target == 'target_image':
        algorithms = representation_algorithms['target_image']

    for key, value in algorithms.items():
        func = eval(key)
        new_img = func(img, value)

    return new_img