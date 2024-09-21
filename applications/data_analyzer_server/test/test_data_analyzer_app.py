import unittest
from unittest.mock import patch
from flask import Flask

from applications.data_analyzer_server.main.data_analyzer_app import visualize_wordcloud, app

class TestDataCollectorApp(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app and push a request context
        self.app = app.test_client()
        self.app.testing = True  # This enables testing mode

    '''
    def test_visualize_wordcloud(self, mock_request, mock_data_analyzer):
        mock_request.json = {'articles_title': 'sample text'}
        mock_data_analyzer_instance = mock_data_analyzer.return_value
        visualize_wordcloud()
        mock_data_analyzer.visualize_wordcloud.assert_called_once_with('sample text')
    '''

    @patch('applications.data_analyzer_server.main.data_analyzer_app.dataAnalyzer.visualize_wordcloud')
    def test_visualize_wordcloud(self, mock_visualize_wordcloud):
        # Mock the behavior of visualize_wordcloud
        mock_visualize_wordcloud.return_value = {"wordcloud": "mocked_result"}

        # Prepare JSON payload
        payload = {'articles_title': 'sample text'}

        # Send a POST request to /wordcloud
        response = self.app.post('/wordcloud', json=payload)

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"wordcloud": "mocked_result"})

        # Ensure visualize_wordcloud was called with the correct parameters
        mock_visualize_wordcloud.assert_called_once_with('sample text')