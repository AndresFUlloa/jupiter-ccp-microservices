
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
    global servidor1_down
    global servidor2_down
    global servidor3_down

    try:
        respuesta=get(target, timeout=3)
        last_digit = 1
        if servidor1_down and tipo == 'principal':
            servidor1_down = False
        elif servidor2_down and tipo == 'redundante 1':
            servidor2_down = False
            last_digit = 2
        response = post('http://127.0.0.1:5006/api/new_url', data={'new_url': 'http://127.0.0.1:500' + last_digit})
        print("El microservicio {} en linea...codigo:".format(tipo), respuesta.status_code)
    except exceptions.ConnectionError:
        print("El microservicio {} esta fuera de servicio, codigo: 400".format(tipo))
        # le comunicamos al API Gateway que no use mas este microservicio porque esta abajo
        last_digit = 2
        if not servidor1_down and tipo == 'principal':
            servidor1_down = True
        elif not servidor2_down and tipo == 'redundante 1':
            servidor2_down = True
            last_digit = 3

        response = post('http://127.0.0.1:5006/api/new_url', data={'new_url': 'http://127.0.0.1:500' + last_digit})
