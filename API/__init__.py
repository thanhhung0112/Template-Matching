from flask import Flask, request
from flask_cors import CORS, cross_origin

from sys import platform
import os

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'