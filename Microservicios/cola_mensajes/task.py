import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('inventario_notify')
queue_name = queue.method.queue

channel.exchange_declare(
    exchange='orden',
    exchange_type='direct'
)

channel.queue_bind(
    exchange='orden',
    queue=queue_name,
    routing_key='inventario.notify'
    )
def callback(ch, method, properties, body):
    payload=json.loads(body)
    print(' [X] Notificando al Inventario ', payload)
    print(' [X] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(on_message_callback=callback, queue=queue_name)

print('[*] Esperando para notificar mensajes. Para salir presione CTRL + C')
channel.start_consuming()