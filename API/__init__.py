from flask import Flask, request

from sys import platform
import os
from ultralytics import YOLO

import logging

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

model = YOLO('Weights/last2.pt', task='segment')