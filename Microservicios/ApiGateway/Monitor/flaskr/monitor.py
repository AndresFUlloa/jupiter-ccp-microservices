import os
import platform
import socket
import struct
import sys
import time
from typing import Tuple
import json
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
        lista_url = None
        if servidor1_down and tipo == 'principal':
            servidor1_down = False
            lista_url = {'new_url': 'http://127.0.0.1:5001'}
        elif servidor2_down and tipo == 'redundante 1':
            servidor2_down = False
            lista_url = {'new_url': 'http://127.0.0.1:5002'}
        if lista_url is not None:
            response = post('http://127.0.0.1:5006/api/new_url', data=json.dumps(lista_url))
        print("El microservicio {} en linea...codigo:".format(tipo), respuesta.status_code)
    except exceptions.ConnectionError:
        print("El microservicio {} esta fuera de servicio, codigo: 400".format(tipo))
        # le comunicamos al API Gateway que no use mas este microservicio porque esta abajo
        lista_url = None
        if not servidor1_down and tipo == 'principal':
            servidor1_down = True
            lista_url = {'new_url': 'http://127.0.0.1:5002'}
        elif not servidor2_down and tipo == 'redundante 1':
            servidor2_down = True
            lista_url = {'new_url': 'http://127.0.0.1:5003'}
        if lista_url is not None:
            response = post('http://127.0.0.1:5006/api/new_url', data=json.dumps(lista_url))
