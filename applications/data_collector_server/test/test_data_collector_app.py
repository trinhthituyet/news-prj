import unittest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime

#with patch('applications.data_collector_server.main.data_collector_app.DataCollectorDB') as MockDataCollectorDB:
with patch('components.data_collector.data_collector_db.DataCollectorDB') as MockDataCollectorDB:
    MockDataCollectorDB.return_value = MagicMock()  

    from applications.data_collector_server.main.data_collector_app import DataCollectorApp


class TestDataCollectorApp(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data='LAST_DAY_RETRIVED=2024-09-15')
    @patch('applications.data_collector_server.main.data_collector_app.DataCollectorDB')
    def test_get_last_retrieve_day_from_file(self, mock_db, mock_file):
        app = DataCollectorApp(url='mock_url')
        last_day = app.get_last_retrieve_day_from_file()
        self.assertEqual(last_day, '2024-09-15')
        mock_file.assert_called_once_with('last_day_info.txt', 'r')
    

    @patch('builtins.open', new_callable=mock_open)
    @patch('applications.data_collector_server.main.data_collector_app.DataCollectorDB')
    def test_update_last_retrieve_day_to_file(self, mock_db, mock_file):
        app = DataCollectorApp(url='mock_url')
        app.update_last_retrieve_day_to_file('2024-09-16')
        mock_file.assert_called_once_with('last_day_info.txt', 'w')
        mock_file().write.assert_called_once_with('LAST_DAY_RETRIVED=2024-09-16\n')


    @patch('applications.data_collector_server.main.data_collector_app.DataCollectorDB')
    @patch('applications.data_collector_server.main.data_collector_app.DataCollector')
    @patch('applications.data_collector_server.main.data_collector_app.DataCollectorApp.update_last_retrieve_day_to_file')
    @patch('applications.data_collector_server.main.data_collector_app.DataCollectorApp.get_last_retrieve_day_from_file', return_value='2024-09-15')
    @patch('applications.data_collector_server.main.data_collector_app.datetime')
    def test_collect_data(self, mock_datetime, mock_get_last_day, mock_update_last_retrieve_day, mock_data_collector, mock_db):
        mock_now = datetime(2024, 9, 16)
        mock_datetime.now.return_value = mock_now
        
        mock_collector_instance = mock_data_collector.return_value
        mock_collector_instance.get_list_of_sources.return_value = ['source1', 'source2']
        mock_collector_instance.retrieve_data.return_value = {'articles': [{'title': 'Test Article'}]}
        
        app = DataCollectorApp(url='mock_url')
        app.collect_data()
        
        mock_collector_instance.get_list_of_sources.assert_called_once_with(language='en', country='us')
        mock_collector_instance.retrieve_data.assert_called_once_with(from_date=mock_get_last_day.return_value, source_list=['source1', 'source2'])
        
        mock_db_instance = mock_db.return_value
        mock_db_instance.save_articles.assert_called_once_with([{'title': 'Test Article'}])
        
        mock_update_last_retrieve_day.assert_called_once()


    @patch('applications.data_collector_server.main.data_collector_app.DataCollectorDB')
    def test_search_text_on_title(self, mock_db):
        mock_db_instance = mock_db.return_value
        mock_db_instance.search_article_title.return_value = ['Article 1', 'Article 2']
        app = DataCollectorApp(url='mock_url')
        app.search_text_on_title('Test')
        mock_db_instance.search_article_title.assert_called_once_with('Test')

if __name__ == '__main__':
    unittest.main()
