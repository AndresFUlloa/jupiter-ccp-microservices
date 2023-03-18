import pika
import json

class ExchangeUtil:
    connection=None
    channel=None

    @staticmethod
    def start_connection():
        ExchangeUtil.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        ExchangeUtil.channel = ExchangeUtil.connection.channel()

    @staticmethod
    def send_message(json_request):
        ExchangeUtil.channel.basic_publish(
            exchange='orden',
            routing_key='inventario.notify',
            body = json.dumps(json_request)
        )
        print(' [X] Notificacion enviada a la bodega')

    @staticmethod
    def close_connection():
        ExchangeUtil.connection.close()