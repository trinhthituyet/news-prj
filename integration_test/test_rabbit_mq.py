'''
import unittest
from unittest.mock import patch, Mock, MagicMock

from applications.application_server.main.main_server import app


with patch('components.data_collector.data_collector_db.DataCollectorDB') as DataCollectorApp:
    DataCollectorApp.return_value = MagicMock()  

    from applications.data_collector_server.main.data_collector_app import init_mq_listener

class TestDataCollectorApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('pika.BlockingConnection')
    def test_main_server_and_data_collector_interact(self, mock_connection):
        mock_channel = Mock()
        mock_connection.return_value.channel.return_value = mock_channel

        #app.run(host='0.0.0.0', port=8080)
        init_mq_listener()

        response = app.post('/send_data_msg_mq', data={"msg": "Test"})
        self.assertEqual(response.data, '<h2>Sent message Test to rabbitmq</h2>')
        mock_channel.basic_ack.assert_called_one()

'''