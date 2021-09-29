import pika, time
from datetime import datetime


def emit_notification(message):
    cred = pika.PlainCredentials('guest', 'guest')
    params = pika.ConnectionParameters(
        host='rabbitmq', # for local -> 'localhost' || for docker -> 'rabbitmq'
        port=5672,
        virtual_host='/',
        credentials=cred
    )
    
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(exchange='logs', exchange_type='fanout')
        channel.basic_publish(
            exchange='logs',
            routing_key='',
            body=message
        )
        print(' [x] Sent %r' % message)
        connection.close()

        return(message)
    
    except:
        print ('[',datetime.now(),'] Could not connect to amqp: Connection refused.\nMessage not sent.')

        return('Message not sent.')

        # # Loop to reconnect  
        # for i in range(3):
        #     if (i==2):
        #           ...
        #     else:
        #         print ('[',datetime.now(),'] amqp connection error.\nTrying again...')
        #         # avoid rapid reconnection on longer RMQ server outage
        #         time.sleep(0.5)
