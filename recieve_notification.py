import pika, time
from datetime import datetime


cred = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(
    host='rabbitmq', # for local -> 'localhost' || for docker -> 'rabbitmq'
    port=5672,
    virtual_host='/',
    credentials=cred
)

while True:
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(exchange='logs', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='logs', queue=queue_name)
        print(' [*] Waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] %r" % body)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError:
        print ('[',datetime.now(),'] Cannot connect to amqp: Connection refused.\nTrying again in 2.00 seconds...')
        # avoid rapid reconnection on longer RMQ server outage
        time.sleep(2) 
