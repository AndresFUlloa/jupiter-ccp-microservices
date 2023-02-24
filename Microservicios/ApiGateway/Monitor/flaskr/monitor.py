
import os
import platform
import socket
import struct
import sys
import time
from typing import Tuple

from requests import get, exceptions

# Monitor de microservicios a traves de request
def monitoreo(target: str, tipo:str):
    try:
        respuesta=get(target, timeout=3)
        print("El microservicio {} en linea...codigo:".format(tipo), respuesta.status_code)
    except exceptions.ConnectionError:
        print("El microservicio {} esta fuera de servicio, codigo: 400".format(tipo))



"""
def icmp_ping(target: str) -> bool:

# Ping the target using ICMP and return True if successful, False otherwise.

    response_time = ping(target, timeout=2)
    print("el tiempo de respuesta da....", response_time)
    return response_time is not None

# if __name__ == "__main__":

def monitoreo(target: str):
    print(f"Pinging {target} every {interval} seconds...")
    while True:
        try:
            is_alive = icmp_ping(target)
            print(is_alive)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {target} is {'up' if is_alive else 'down'}")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("Stopping ICMP monitoring...")
            break

"""