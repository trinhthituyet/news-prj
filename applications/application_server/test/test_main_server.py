import os, sys
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from applications.application_server.main.main_server import app

sys.path.insert(0, os.path.abspath("."))
print(os.path.abspath("."))

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('applications.application_server.main.main_server.db_collector.search_article_title')
    def test_search_articles(self, mock_search):
        # Mock the search_article_title method
        mock_search.return_value = [
            {"_source": {"title": "Test Article 1"}},
            {"_source": {"title": "Test Article 2"}}
        ]

        # Simulate a POST request to /search_articles with form data
        response = self.app.post("/search_articles", data={"user_input": "Test"})

        # Verify the db_collector method was called with correct arguments
        mock_search.assert_called_once_with("Test")

        # Check that the correct template is rendered and articles are passed
        self.assertIn(b'Test Article 1', response.data)
        self.assertIn(b'Test Article 2', response.data)

    @patch('applications.application_server.main.main_server.db_collector.search_article_last_n_days')
    def test_search_articles_last_7_days(self, mock_search):
        # Mock the search_article_last_n_days method
        mock_search.return_value = [
            {"_source": {"title": "Test Article 3"}},
            {"_source": {"title": "Test Article 4"}}
        ]

        # Simulate a POST request to /articles_last_7_days
        response = self.app.post("/articles_last_7_days")

        # Verify the db_collector method was called with the correct argument
        mock_search.assert_called_once_with(7)

        # Check that the correct template is rendered and articles are passed
        self.assertIn(b'Test Article 3', response.data)
        self.assertIn(b'Test Article 4', response.data)

    @patch('applications.application_server.main.main_server.db_collector.search_article_last_n_days')
    def test_search_articles_last_30_days(self, mock_search):
        # Mock the search_article_last_n_days method
        mock_search.return_value = [
            {"_source": {"title": "Test Article 5"}},
            {"_source": {"title": "Test Article 6"}}
        ]

        # Simulate a POST request to /articles_last_30_days
        response = self.app.post("/articles_last_30_days")

        # Verify the db_collector method was called with the correct argument
        mock_search.assert_called_once_with(30)

        # Check that the correct template is rendered and articles are passed
        self.assertIn(b'Test Article 5', response.data)
        self.assertIn(b'Test Article 6', response.data)

    @patch('applications.application_server.main.main_server.mq_worker.send_msg')
    def test_collect_data(self, mock_send_msg):
        # Simulate a POST request to /collect_data
        response = self.app.post("/collect_data")

        # Verify the mq_worker's send_msg method was called with 'collect'
        mock_send_msg.assert_called_once_with('collect')

        # Check the correct response is returned
        self.assertIn(b'Sent message to data collector', response.data)

if __name__ == "__main__":
    unittest.main()
