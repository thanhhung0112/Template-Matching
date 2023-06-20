from flask import Flask, request

from sys import platform
import os
from ultralytics import YOLO
import numpy as np
from Utils.load_image import TurboJpegLoader

import logging

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

model = YOLO('Weights/last2.pt', task='segment')

transformation_matrix = np.load('Calib/transformation_matrix.npy')

loader = TurboJpegLoader()