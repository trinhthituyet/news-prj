#get data from News API
import requests

class DataCollector:
    def __init__(self, api_key):
        self.api_key = api_key

    def retrieve_data_page(self, from_date, source_list, page):
        url = 'https://newsapi.org/v2/everything'
        params = {
            #'q': 'artificial intelligence',
            'from': from_date,
            #'domains': '',
            'sources': source_list,
            'language': 'en',
            'sortBy': 'popularity',
            'apiKey': self.api_key,
            'page': page
        }
        if from_date == "0000-00-00":
            del params['from']
        response = requests.get(url, params=params)
        data = response.json()
        return data        

    def retrieve_data(self, from_date, source_list):
        page = 1
        data = []
        while True:
            data_page = self.retrieve_data_page(from_date, source_list, page)
            if  data_page['status'] == 'ok':
                #print("data: ", data_page['articles'])
                print("page: ", page)
            if data_page['status'] == 'error':
                print("Collecting error: ", data_page['message'])
                return 'error', data
            elif len(data_page['articles']) == 0:
                return 'ok', data
            else:
                data.extend(data_page['articles'])
                page += 1
    
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