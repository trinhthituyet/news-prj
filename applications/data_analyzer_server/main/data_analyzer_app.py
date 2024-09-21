import sys, os
from flask import Flask, request
from flask_cors import CORS

sys.path.insert(0, os.path.abspath("."))
print(os.path.abspath("."))

from components.data_analyzer.data_analyzer_core import DataAnalyzer

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8080"}})
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