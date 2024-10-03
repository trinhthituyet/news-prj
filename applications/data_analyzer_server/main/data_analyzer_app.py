import sys, os
from flask import Flask, request
from flask_cors import CORS

sys.path.insert(0, os.path.abspath("."))
print(os.path.abspath("."))

from components.data_analyzer.data_analyzer_core import DataAnalyzer

def read_main_svr_ip():
    with open('config.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
            if line.startswith('MAIN_SERVER_IP'):
                main_svr_ip = line.strip().split('=')[1]
                print("main_svr_ip: ", main_svr_ip)
                return main_svr_ip

app = Flask(__name__)
main_svr_ip = read_main_svr_ip()
CORS(app, resources={r"/*": {"origins": "http://" + main_svr_ip + ":8080"}})
dataAnalyzer = DataAnalyzer()

@app.route("/wordcloud", methods=["POST"])
def visualize_wordcloud():
    #text = session.get('articles_title', '')
    text = request.json.get('articles_title', '')
    #print(request.json)
    #print("wordcloud text: ", text)
    return dataAnalyzer.visualize_wordcloud(text)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8088)