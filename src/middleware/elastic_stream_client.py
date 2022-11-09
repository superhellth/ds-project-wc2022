import tweepy
import elasticsearch
import twitter_tweet
import json


class ElasticStreamClient(tweepy.StreamingClient):
    """Our custom StreamingClient class, to forward incoming tweets to our elasticsearch index"""

    def __init__(self, bearer_token, elastic_client: elasticsearch.Elasticsearch, index_name: str):
        self.es_client = elastic_client
        self.index_name = index_name
        self.count = 0
        super().__init__(bearer_token=bearer_token, wait_on_rate_limit=True)

    def on_data(self, raw_data):
        """This is how we process tweets"""
        self.count += 1
        print(f"Tweet received! This is number {self.count}")
        raw_data = json.loads(raw_data)
        tweet = twitter_tweet.Tweet(raw_data)
        resp = self.es_client.index(
            index=self.index_name, document=tweet.get_as_es_doc(), id=tweet.get_id())
        return super().on_tweet(raw_data)
