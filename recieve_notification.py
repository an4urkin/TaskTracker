import pika

# for local ->'amqp://guest:guest@localhost:5672/%2F' // for docker -> 'amqp://guest:guest@rabbitmq:5672'
params = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F') 
connection = pika.BlockingConnection(params)  # pika.ConnectionParameters(host='localhost')
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
