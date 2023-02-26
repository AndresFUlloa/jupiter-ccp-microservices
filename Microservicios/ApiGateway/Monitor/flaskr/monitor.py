
import os
import platform
import socket
import struct
import sys
import time
from typing import Tuple

from requests import get, exceptions, post

servidor1_down = False
servidor2_down = False
servidor3_down = False

# Monitor de microservicios a traves de request
def monitoreo(target: str, tipo:str):
    try:
        respuesta=get(target, timeout=3)
        print("El microservicio {} en linea...codigo:".format(tipo), respuesta.status_code)
    except exceptions.ConnectionError:
        print("El microservicio {} esta fuera de servicio, codigo: 400".format(tipo))
        # le comunicamos al API Gateway que no use mas este microservicio porque esta abajo
        response = post('http://127.0.0.1:5006/api/new_url', data = {'new_url':'http://127.0.0.1:5002'})

