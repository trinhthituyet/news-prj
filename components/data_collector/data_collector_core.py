#get data from News API
import requests

class DataCollector:
    def __init__(self, api_key):
        self.api_key = api_key

    def retrieve_data(self, from_date, source_list):
        url = 'https://newsapi.org/v2/everything'
        params = {
            #'q': 'artificial intelligence',
            'from': from_date,
            #'domains': '',
            'sources': source_list,
            'language': 'en',
            'sortBy': 'popularity',
            'apiKey': self.api_key,
        }
        if from_date == "0000-00-00":
            del params['from']
        response = requests.get(url, params=params)
        data = response.json()
        return data
    
    def get_list_of_sources(self, category=None, language=None, country=None):
        url = 'https://newsapi.org/v2/top-headlines/sources'
        params = {
            'apiKey': self.api_key
        }
        if category != None:
            params['category'] = category
        if language != None:
            params['language'] = language
        if country != None:
            params['country'] = country

        response = requests.get(url, params=params)
        data = response.json()

        source_ids = []
        for source in data['sources']:
            source_ids.append(source['id'])

        return source_ids