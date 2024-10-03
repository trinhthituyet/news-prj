import pika
import time

class RabbitMQWorker:
    def __init__(self, host):
        self.host = host
        self.connect()
    
    def connect(self):
        try:
            connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, heartbeat=300))
            self.channel = connection.channel()
            self.channel.queue_declare(queue='data_collector_queue', durable=True)
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection failed, retrying... {e}")
            time.sleep(2)
            self.connect()

    def send_msg(self, message):
        print("RabbitMQWorker send_msg")
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key='data_collector_queue',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
            ))
        #except pika.exceptions.ConnectionClosed:
        except Exception as e:
            print("basic_publish error occurred: ", str(e))
            print("Connection closed, reconnecting...")
            self.connect()
            self.send_msg(message)