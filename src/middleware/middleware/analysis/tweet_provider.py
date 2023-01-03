from elasticsearch import helpers, Elasticsearch
from middleware.tweet_management import twitter_tweet


class TweetProvider:

    def __init__(self):
        self.es_client = Elasticsearch(
            "http://45.13.59.173:9200", http_auth=("elastic", "sicheristsicher"))
        self.index = "tweets"

    def get_tweet_list(self, size=100, body={"match_all": {}}):
        """Returns a list of tweet objects of size size."""
        tweets = list()
        response = self.es_client.search(index=self.index, size=size, body=body, timeout="1m", request_timeout=30)
        for tweet in response["hits"]["hits"]:
            tweets.append(twitter_tweet.Tweet(tweet, is_es_doc=True))
        return tweets

    def get_corpus(self, size=100):
        """Returns a list of strings of size size."""
        corpus = list()
        for document in helpers.scan(self.es_client, index=self.index, _source=["text"]):
            corpus.append(document["_source"]["text"])
            if len(corpus) == size:
                break
        return corpus

    def get_client(self):
        """Returns a connection to the elasticsearch server"""
        return self.es_client
