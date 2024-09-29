#store data to DB
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class DataCollectorDB:
    article_index = "articles-index"
    es = None
    def __init__(self, urls):
        self.es = Elasticsearch(urls)
        '''
        setting = {
            "settings": {
                "index": {
                    "number_of_shards": 1,    # Number of primary shards
                    "number_of_replicas": 0   # Number of replica shards
                }
            },
            "mappings": {
                "properties": {
                    "source_id": {"type": "text"},
                    "source_name": {"type": "text"},
                    "author": {"type": "text"}, 
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "url": {"type": "text"},
                    "urlToImage": {"type": "text"},
                    "publishedAt": {"type": "text"},
                    "content": {"type": "text"}
                }
            }
        }
        '''

        # Create the index with the mapping
        #self.es.indices.create(index=self.article_index, body=setting)
        if not self.es.indices.exists(index=self.article_index):
            self.es.indices.create(index=self.article_index)
        

    def save_articles(self, articles):
        actions = []
        for article in articles:
            print("ARTICLE: ", article)
            article["source_id"] = article["source"]["id"]
            article["source_name"] = article["source"]["name"]
            del article["source"]
            actions.append({
                "_index": self.article_index,
                "_source": article
            })
        
        success, failed = bulk(self.es, actions)
        print("success: ", success)
        print("fail: ", failed)

    def search_article_title(self, search_text):
        query = {
            "query": {
                "match": {
                    "title": search_text
                }
            },
            "size": 10000
        }

        response = self.es.search(index=self.article_index, body=query)

        return response['hits']['hits']
    
    def search_article_last_n_days(self, n):
        mapping = self.es.indices.get_mapping(index=self.article_index)

        # Print the mapping schema
        print(mapping)

        query = {
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

        response = self.es.search(index=self.article_index, body=query)

        return response['hits']['hits']