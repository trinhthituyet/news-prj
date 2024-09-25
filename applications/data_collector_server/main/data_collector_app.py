import os, sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pika

sys.path.insert(0, os.path.abspath("."))
print(os.path.abspath("."))
load_dotenv()

from components.data_collector.data_collector_core import DataCollector
from components.data_collector.data_collector_db import DataCollectorDB


class DataCollectorApp:
    def __init__(self, url):
        self.collector_db = DataCollectorDB(url)

    def get_last_retrieve_day_from_file(self):
        with open('last_day_info.txt', 'r') as file:
            lines = file.readlines()

        for line in lines:
                if line.startswith('LAST_DAY_RETRIVED'):
                    last_day = line.strip().split('=')[1]
                    return last_day
                
    def update_last_retrieve_day_to_file(self, last_day):
        with open('last_day_info.txt', 'w') as file:
            file.write(f'LAST_DAY_RETRIVED={last_day}\n')

    def collect_data(self):
        api_key = os.environ['API_KEY']
        last_date = self.get_last_retrieve_day_from_file()
        current_datetime = datetime.now()  - timedelta(days=1)
        #print("current datetime: ", current_datetime)
        data_collector = DataCollector(api_key=api_key)
        source_ids = data_collector.get_list_of_sources(language='en', country='us')
        data = data_collector.retrieve_data(from_date=last_date, source_list=source_ids)
        #print(data)
        self.collector_db.save_articles(data['articles'])
        current_datetime_str = current_datetime.isoformat()
        #os.environ['LAST_DAY_RETRIVED'] = current_datetime_str
        self.update_last_retrieve_day_to_file(current_datetime_str)

    def search_text_on_title(self, text):
        res = self.collector_db.search_article_title(text)
        print(res)

def callback(ch, method, properties, body):
    msg = body.decode()
    print(f" [x] Received {msg}")
    if msg == "":
        app.collect_data()
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)        

def init_mq_listener():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='data_collector_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='data_collector_queue', on_message_callback=callback)

    channel.start_consuming()


app = DataCollectorApp("http://localhost:9200")

if __name__ == "__main__":
    init_mq_listener()
    #app.collect_data()
    #app.search_text_on_title("Kamala")