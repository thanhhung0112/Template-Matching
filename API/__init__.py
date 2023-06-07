from flask import Flask, request
from flask_cors import CORS, cross_origin

from sys import platform
import os
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

model = YOLO('Weights/last2.pt')