import os
import platform
import socket
import struct
import sys
import time
from typing import Tuple
import json
from requests import get, exceptions, post
from .log_utils import LogUtils

servidor1_down = False
servidor2_down = False
servidor3_down = False
current_url = 'http://127.0.0.1:5001'

# Monitor de microservicios a traves de request
def monitoreo(target: str, tipo:str):
    global servidor1_down
    global servidor2_down
    global servidor3_down
    global current_url

    try:
        respuesta=get(target, timeout=3)

        lista_url = None
        if servidor1_down and tipo == 'principal':
            servidor1_down = False
            lista_url = {'new_url': current_url}
            LogUtils.write_message('Server: {} is up'.format(target))
        elif servidor2_down and tipo == 'redundante 1':
            servidor2_down = False
            LogUtils.write_message('Server: {} is up'.format(target))
            if current_url == 'http://127.0.0.1:5003':
                current_url = 'http://127.0.0.1:5002'
                lista_url = {'new_url': current_url}
        elif servidor3_down and tipo == 'redundante 2':
            servidor3_down = False
            LogUtils.write_message('Server: {} is up'.format(target))

        if lista_url is not None:
            response = post('http://127.0.0.1:5006/api/new_url', data=json.dumps(lista_url))
            LogUtils.write_message('Se cambio el servidor: {}'. format(current_url))
        print("El microservicio {} en linea...codigo:".format(tipo), respuesta.status_code)
    except exceptions.ConnectionError:
        if target == (current_url + "/ventas"):
            LogUtils.write_message('Server: {} is down'.format(target))
        print("El microservicio {} esta fuera de servicio, codigo: 400".format(tipo))
       # le comunicamos al API Gateway que no use mas este microservicio porque esta abajo
        lista_url = None
        if not servidor1_down and tipo == 'principal':
            servidor1_down = True
            LogUtils.write_message('Server: {} is down'.format(target))
            if current_url == 'http://127.0.0.1:5001':
                if not servidor2_down:
                    current_url = 'http://127.0.0.1:5002'
                    lista_url = {'new_url': current_url}
                else:
                    current_url = 'http://127.0.0.1:5003'
                    lista_url = {'new_url': current_url}
        elif not servidor2_down and tipo == 'redundante 1':
            servidor2_down = True
            LogUtils.write_message('Server: {} is down'.format(target))
            if servidor1_down:
                current_url = 'http://127.0.0.1:5003'
                lista_url = {'new_url': current_url}
        elif not servidor3_down and tipo == 'redundante 2':
            servidor3_down = True
            LogUtils.write_message('Server: {} is down'.format(target))

        if lista_url is not None:
            response = post('http://127.0.0.1:5006/api/new_url', data=json.dumps(lista_url))
            LogUtils.write_message('Se cambio al servidor: {}'.format(current_url))

