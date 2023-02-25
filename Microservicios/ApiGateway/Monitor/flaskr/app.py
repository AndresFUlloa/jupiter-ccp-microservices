from flaskr import create_app
from .monitor import monitoreo
from flask_restful import Api
from ping3 import ping, verbose_ping


app = create_app('default')
app_context = app.app_context()
app_context.push()


with app.app_context():
    #print(verbose_ping('http://0.0.0.0:5001/ventas', count=0, interval=1))
    while True:
        try:
            monitoreo("http://127.0.0.1:5001/ventas", "principal")
            monitoreo("http://127.0.0.1:5002/ventas", "redundante 1")
            monitoreo("http://127.0.0.1:5003/ventas", "redundante 2")
            monitoreo("http://127.0.0.1:5004/prueba", "principal-comandos")

        except KeyboardInterrupt:
            print("Stopping ICMP monitoring...")
            break
