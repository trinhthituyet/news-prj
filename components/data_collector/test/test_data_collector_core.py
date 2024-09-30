import unittest
from unittest.mock import patch
from components.data_collector.data_collector_core import DataCollector  # Assuming your class is saved as data_collector.py

class TestDataCollector(unittest.TestCase):
    
    def setUp(self):
        self.api_key = 'test_api_key'
        self.data_collector = DataCollector(self.api_key)
    
    @patch('requests.get')
    def test_retrieve_data_page(self, mock_get):
        # Define the mock response
        mock_response = {'articles': [
                {'title': 'AI is transforming the world', 'source': {'name': 'TechCrunch'}},
                {'title': 'The future of AI', 'source': {'name': 'Wired'}}
            ]}
       
        # Mock requests.get to return the mock_response
        mock_get.return_value.json.return_value = mock_response

        from_date = '2023-01-01'
        source_list = 'techcrunch,wired'
        
        # Call the retrieve_data method
        data = self.data_collector.retrieve_data_page(from_date, source_list, 1)
        
        # Assertions
        self.assertEqual(len(data['articles']), 2)
        self.assertEqual(data['articles'][0]['title'], 'AI is transforming the world')
        self.assertEqual(mock_get.call_count, 1)
        mock_get.assert_called_with(
            'https://newsapi.org/v2/everything', 
            params={
                'from': '2023-01-01',
                'sources': 'techcrunch,wired',
                'language': 'en',
                'sortBy': 'popularity',
                'apiKey': self.api_key,
                'page': 1
            }
        )
    
    @patch('requests.get')
    def test_get_list_of_sources(self, mock_get):
        # Define the mock response
        mock_response = {
            'status': 'ok',
            'sources': [
                {'id': 'techcrunch', 'name': 'TechCrunch'},
                {'id': 'wired', 'name': 'Wired'}
            ]
        }
        # Mock requests.get to return the mock_response
        mock_get.return_value.json.return_value = mock_response

        # Call the get_list_of_sources method
        status, sources = self.data_collector.get_list_of_sources(language='en', category='technology')
        
        # Assertions
        self.assertEqual(status, 'ok')
        self.assertEqual(sources, ['techcrunch', 'wired'])
        self.assertEqual(mock_get.call_count, 1)
        mock_get.assert_called_with(
            'https://newsapi.org/v2/top-headlines/sources', 
            params={
                'apiKey': self.api_key,
                'category': 'technology',
                'language': 'en'
            }
        )

if __name__ == '__main__':
    unittest.main()
