# news-prj
Collect and analyze data from NewsAPI

1. Set up environment
   - Visit https://newsapi.org/ to create an account and obtain your API key. Add this key to environment variables
   - Open the config.txt file and update the following variables with the correct values:
      + LAST_DAY_RETRIEVED: For the first data collection from NewsAPI, set this to '0000-00-00'. This value will automatically update after each successful data collection.
      + MAIN_SERVER_IP: Enter the correct IP address for the main server.
      + DATA_ANALYZER_IP: Enter the correct IP address for the data analyzer.
2. How to run
   - Run docker-compose to start RabbitMQ and ElasticSearchDB.
   - Run ./start.sh for start all 3 components: DataCollector, DataAnalyzer, MainServer
