import os, sys
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
#from applications.application_server.main.main_server import app

#sys.path.insert(0, os.path.abspath("."))
#print(os.path.abspath("."))
#with patch('applications.application_server.main.main_server.DataCollectorDB') as MockDataCollectorDB, \
    #patch('applications.application_server.main.main_server.RabbitMQWorker') as MockRabbitMQWorker:
with patch('components.data_collector.data_collector_db.DataCollectorDB') as MockDataCollectorDB, \
     patch('applications.application_server.main.mq_worker.RabbitMQWorker') as MockRabbitMQWorker:
    
    # Mock the instances of the classes
    MockDataCollectorDB.return_value = MagicMock()
    
    MockRabbitMQWorker.return_value = MagicMock()

    # Now import the app after mocking
    from applications.application_server.main.main_server import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('applications.application_server.main.main_server.db_collector.search_article_title')
    def test_search_articles(self, mock_func):
        mock_func.return_value = [
            {"_source": {"title": "Test Article 1"}},
            {"_source": {"title": "Test Article 2"}}
        ]

        response = self.app.post("/search_articles", data={"user_input": "Test"})

        mock_func.assert_called_once_with("Test")

        # Check that the correct template is rendered and articles are passed
        self.assertIn(b'Test Article 1', response.data)
        self.assertIn(b'Test Article 2', response.data)

    @patch('applications.application_server.main.main_server.db_collector')
    def test_search_articles_last_7_days(self, mock_db_collector):
        mock_db_collector.search_article_last_n_days.return_value = [
            {"_source": {"title": "Test Article 3"}},
            {"_source": {"title": "Test Article 4"}}
        ]

        response = self.app.post("/articles_last_7_days")

        mock_db_collector.search_article_last_n_days.assert_called_once_with(7)

        self.assertIn(b'Test Article 3', response.data)
        self.assertIn(b'Test Article 4', response.data)

    @patch('applications.application_server.main.main_server.db_collector')
    def test_search_articles_last_30_days(self, mock_db_collector):
        mock_db_collector.search_article_last_n_days.return_value = [
            {"_source": {"title": "Test Article 5"}},
            {"_source": {"title": "Test Article 6"}}
        ]

        response = self.app.post("/articles_last_30_days")

        mock_db_collector.search_article_last_n_days.assert_called_once_with(30)

        self.assertIn(b'Test Article 5', response.data)
        self.assertIn(b'Test Article 6', response.data)

    @patch('applications.application_server.main.main_server.mq_worker.send_msg')
    def test_collect_data(self, mock_send_msg):
        response = self.app.post("/collect_data")

        mock_send_msg.assert_called_once_with('collect')

        self.assertIn(b'Sent message to data collector', response.data)

if __name__ == "__main__":
    unittest.main()
