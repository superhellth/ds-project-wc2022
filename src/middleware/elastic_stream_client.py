import tweepy
import elasticsearch
import twitter_tweet


class ElasticStreamClient(tweepy.StreamingClient):
    """Our custom StreamingClient class, to forward incoming tweets to our elasticsearch index"""

    def __init__(self, bearer_token, elastic_client: elasticsearch.Elasticsearch, index_name: str):
        self.es_client = elastic_client
        self.index_name = index_name
        super().__init__(bearer_token)

    def on_tweet(self, tweet):
        """This is how we process tweets"""
        print("Tweet received!")
        tweet_ = twitter_tweet.Tweet(tweet)
        resp = self.es_client.index(
            index=self.index_name, document=tweet_.get_as_es_doc(), id=tweet_.get_id())
        return super().on_tweet(tweet)
