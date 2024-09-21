import unittest
from unittest.mock import patch, MagicMock, Mock
from components.data_collector.data_collector_db import DataCollectorDB

class TestDataCollectorDB(unittest.TestCase):
    
    @patch('components.data_collector.data_collector_db.bulk')  # Mock the bulk helper
    @patch('components.data_collector.data_collector_db.Elasticsearch')
    def test_save_articles(self, mock_es, mock_bulk):
        # Arrange
        mock_es_instance = mock_es.return_value  # Mock Elasticsearch instance

        mock_bulk.return_value = (5, 0)  # Mock bulk success and failed counts
        '''
        print("Mock name:", mock_bulk._mock_name)               # Name of the mock (if any)
        print("Mock calls:", mock_bulk.mock_calls)              # List of all calls made to the mock
        print("Mock method calls:", mock_bulk.method_calls)     # List of method calls
        print("Mock attributes:", dir(mock_bulk))               # List all attributes of the mock object
        print("Mock return value:", mock_bulk.return_value)     # The default return value (can be set)
        '''
        
        db = DataCollectorDB(urls='http://localhost:9200')
        articles = [
            {
                "source": {"id": "source1", "name": "Source Name"},
                "author": "Author 1",
                "title": "Test Title 1",
                "description": "Description 1",
                "url": "http://example.com/1",
                "urlToImage": "http://example.com/image1",
                "publishedAt": "2024-09-12",
                "content": "Content 1"
            },
            {
                "source": {"id": "source2", "name": "Source Name 2"},
                "author": "Author 2",
                "title": "Test Title 2",
                "description": "Description 2",
                "url": "http://example.com/2",
                "urlToImage": "http://example.com/image2",
                "publishedAt": "2024-09-13",
                "content": "Content 2"
            }
        ]
        
        # Act
        db.save_articles(articles)

        # Assert
        # Check that the articles were processed into actions correctly
        expected_actions = [
            {
                "_index": db.article_index,
                "_source": {
                    "source_id": "source1",
                    "source_name": "Source Name",
                    "author": "Author 1",
                    "title": "Test Title 1",
                    "description": "Description 1",
                    "url": "http://example.com/1",
                    "urlToImage": "http://example.com/image1",
                    "publishedAt": "2024-09-12",
                    "content": "Content 1"
                }
            },
            {
                "_index": db.article_index,
                "_source": {
                    "source_id": "source2",
                    "source_name": "Source Name 2",
                    "author": "Author 2",
                    "title": "Test Title 2",
                    "description": "Description 2",
                    "url": "http://example.com/2",
                    "urlToImage": "http://example.com/image2",
                    "publishedAt": "2024-09-13",
                    "content": "Content 2"
                }
            }
        ]

        mock_bulk.assert_called_once_with(mock_es_instance, expected_actions)


    @patch('components.data_collector.data_collector_db.Elasticsearch')
    def test_search_article_title(self, mock_es):
        # Arrange
        mock_es_instance = mock_es.return_value
        mock_es_instance.search.return_value = {
            'hits': {
                'hits': [
                    {'_source': {'title': 'Test Title 1', 'content': 'Content 1'}},
                    {'_source': {'title': 'Test Title 2', 'content': 'Content 2'}}
                ]
            }
        }

        db = DataCollectorDB(urls=['http://localhost:9200'])
        search_text = 'Test'

        # Act
        result = db.search_article_title(search_text)

        # Assert
        expected_query = {
            "query": {
                "match": {
                    "title": search_text
                }
            },
            "size": 10000
        }

        mock_es_instance.search.assert_called_once_with(index=db.article_index, body=expected_query)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['_source']['title'], 'Test Title 1')
        self.assertEqual(result[1]['_source']['title'], 'Test Title 2')

    @patch('components.data_collector.data_collector_db.Elasticsearch')
    def test_search_article_last_n_days(self, mock_es):
        mock_es_instance = mock_es.return_value
        mock_es_instance.search.return_value = {
            'hits': {
                'hits': [
                    {'_source': {'publishedAt': '2024-09-12', 'title': 'Test Title 1'}},
                    {'_source': {'publishedAt': '2024-09-13', 'title': 'Test Title 2'}}
                ]
            }
        }

        db = DataCollectorDB(urls=['http://localhost:9200'])
        n = 7  # Search for the last 7 days

        # Act
        result = db.search_article_last_n_days(n)

        # Assert
        expected_query = {
            "query": {
                "range": {
                    "publishedAt": {
                        "gte": f"now-{n}d",
                        "lte": "now"
                    }
                }
            },
            "size": 10000
        }

        mock_es_instance.search.assert_called_once_with(index=db.article_index, body=expected_query)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['_source']['publishedAt'], '2024-09-12')
        self.assertEqual(result[1]['_source']['publishedAt'], '2024-09-13')
