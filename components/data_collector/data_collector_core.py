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
        source_list_str = ",".join(source_list)
        while True:
            data_page = self.retrieve_data_page(from_date, source_list_str, page)
            print("page: ", page)
            print("data_page: ", data_page)
            if  data_page['status'] == 'ok':
                print("data len: ", len(data_page['articles']))
                
            if data_page['status'] == 'error':
                print("Collecting error: ", data_page['message'])
                if 'Developer accounts are limited' in data_page['message']:
                    return 'ok', data
                else:
                    return 'error', []
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
        if data['status'] == 'error':
            print('get_list_of_sources error: ', data['message'])
            return 'error', []

        source_ids = []
        for source in data['sources']:
            source_ids.append(source['id'])

        return 'ok', source_ids