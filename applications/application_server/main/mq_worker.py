import pika

class RabbitMQWorker:
    def __init__(self, host):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, heartbeat=300))
        self.channel = connection.channel()

        self.channel.queue_declare(queue='data_collector_queue', durable=True)

    def send_msg(self, message):
        print("RabbitMQWorker send_msg")
        self.channel.basic_publish(
            exchange='',
            routing_key='data_collector_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
        ))