from wordcloud import WordCloud
import matplotlib.pyplot as plt
from flask import send_file
import io


class DataAnalyzer:
    def __init__(self):
        return None
    
    def visualize_wordcloud(self, text):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        # Save the word cloud image to a BytesIO object
        img = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(img, format='PNG')
        img.seek(0)

        # Send the image to the client
        return send_file(img, mimetype='image/png')
    
    def analyze_trend(self, text):
        return None