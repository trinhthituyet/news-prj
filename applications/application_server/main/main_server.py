#!/usr/bin/env python3

import os, sys
from flask import Flask, request, render_template

sys.path.insert(0, os.path.abspath("."))
print(os.path.abspath("."))

from prometheus_flask_exporter import PrometheusMetrics
from components.data_collector.data_collector_db import DataCollectorDB
from applications.application_server.main.mq_worker import RabbitMQWorker

app = Flask(__name__)
app.secret_key = "tuyet"

metrics = PrometheusMetrics(app)

db_collector = DataCollectorDB("http://localhost:9200")

mq_worker = RabbitMQWorker('localhost')

def read_analyzer_ip():
    with open('config.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
            if line.startswith('DATA_ANALYZER_IP'):
                analyzer_ip = line.strip().split('=')[1]
                print("analyzer_ip: ", analyzer_ip)
                return analyzer_ip
            
wordcloud_url = "http://" + read_analyzer_ip() + ":8088/wordcloud"   

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/search_articles", methods=["POST"])
def search_articles():
    input_text = request.form.get("user_input", "")
    print("You entered: " + input_text)
    articles = db_collector.search_article_title(input_text)
    return render_template("articles.html", articles = articles, wordcloud_url = wordcloud_url)

@app.route("/articles_last_7_days", methods=["POST"])
def search_articles_last_7_days():
    articles = db_collector.search_article_last_n_days(7)
    return render_template("articles.html", articles = articles, wordcloud_url = wordcloud_url)

@app.route("/articles_last_30_days", methods=["POST"])
def search_articles_last_30_days():
    articles = db_collector.search_article_last_n_days(30)
    return render_template("articles.html", articles = articles, wordcloud_url = wordcloud_url)

@app.route("/collect_data", methods=["POST"])
def collect_data():
    mq_worker.send_msg('collect')
    return 'Sent message to data collector successfully'

@app.route("/send_data_msg_mq", methods=["POST"])
def send_data_msg_mq():
    data = request.get_json()
    msg = data['msg']
    mq_worker.send_msg(msg)
    return '<h2>Sent message {msg} to rabbitmq</h2>'
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
