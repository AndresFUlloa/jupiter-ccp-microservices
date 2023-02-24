import os
import platform
import socket
import struct
import sys
import time
from typing import Tuple
from ping3 import ping

# Set the target IP address or hostname of the microservice you want to monitor
target = "example.com"

# Set the interval in seconds between each ping request
interval = 1

def icmp_ping(target: str) -> bool:
    """
    Ping the target using ICMP and return True if successful, False otherwise.
    """
    response_time = ping(target, timeout=2)
    return response_time is not None

if __name__ == "__main__":
    print(f"Pinging {target} every {interval} seconds...")
    while True:
        try:
            is_alive = icmp_ping(target)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {target} is {'up' if is_alive else 'down'}")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("Stopping ICMP monitoring...")
            break