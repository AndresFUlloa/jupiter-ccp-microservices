from flask import Flask
import os
import platform
import socket
import struct
import sys
import time
from typing import Tuple


def create_app(config_name):
    app = Flask(__name__)
    return app
