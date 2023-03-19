import pika
import json

class ExchangeUtil:
    connection=None
    channel=None

    @staticmethod
    def start_connection():
        ExchangeUtil.connection = pika.BlockingConnection(pika.URLParameters(('amqps://rxrfnebd:p2RNcqtzpqchcVfPZ2gKd-uyCX1Q3yM0@jackal.rmq.cloudamqp.com/rxrfnebd')))
        ExchangeUtil.channel = ExchangeUtil.connection.channel()
        queue = ExchangeUtil.channel.queue_declare('inventario_notify')
        queue_name = queue.method.queue
        ExchangeUtil.channel.queue_bind(
            exchange='orden',
            queue=queue_name,
            routing_key='inventario.notify'
        )

    @staticmethod
    def send_message(json_request, token):
        headers = {'token':token}
        ver_publicacion=ExchangeUtil.channel.basic_publish(
            exchange='orden',
            routing_key='inventario.notify',
            body = json.dumps(json_request),
            properties = pika.BasicProperties(headers=headers)
        )
        print(' [X] Notificacion enviada a la bodega de Jesus', ver_publicacion)

    @staticmethod
    def close_connection():
        ExchangeUtil.connection.close()