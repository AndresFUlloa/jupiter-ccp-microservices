from celery import Celery

app_ventas = Celery('tasks', broker='amqp://guest@localhost//')

@app_ventas.task
def process_request(request_json):
    # Procesar el mensaje aquí
   print(request_json)
