import pika
import json
import requests

connection = pika.BlockingConnection(pika.URLParameters(('amqps://rxrfnebd:p2RNcqtzpqchcVfPZ2gKd-uyCX1Q3yM0@jackal.rmq.cloudamqp.com/rxrfnebd')))
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
    print(payload)
    encabezados = {'Content-Type':'application/json', 'Authorization':properties.headers.get('token', 'default-value')}
    response = requests.post('http://localhost:5006/actualizar_venta/' + str(payload['venta_id']), data=json.dumps(payload),headers=encabezados)
    print(' [X] Notificando al Inventario ', payload, response)
    print(' [X] Done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(on_message_callback=callback, queue=queue_name)

print('[*] Esperando para notificar mensajes. Para salir presione CTRL + C')
channel.start_consuming()