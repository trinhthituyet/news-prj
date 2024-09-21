import unittest
from unittest.mock import patch, MagicMock
from components.data_analyzer.data_analyzer_core import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):

    @patch('components.data_analyzer.data_analyzer_core.send_file')  # Mocking send_file
    @patch('components.data_analyzer.data_analyzer_core.plt')  # Mocking plt
    @patch('wordcloud.WordCloud.generate')  # Mocking WordCloud
    def test_visualize_wordcloud(self, mock_wordcloud_generate, mock_plt, mock_send_file):
        # Setup
        mock_wordcloud_generate.return_value = MagicMock()
        mock_send_file.return_value = 'mocked_response'

        text = "visualized text"
        
        analyzer = DataAnalyzer()

        response = analyzer.visualize_wordcloud(text)

        mock_wordcloud_generate.assert_called_once_with(text)
        mock_plt.savefig.assert_called_once()
        self.assertEqual(response, 'mocked_response')


if __name__ == '__main__':
    unittest.main()
