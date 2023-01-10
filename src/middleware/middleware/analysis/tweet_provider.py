import queue
from elasticsearch import helpers, Elasticsearch
from middleware.tweet_management import twitter_tweet


class TweetProvider:
    """This class provides tweets from ES either as tweet objects or as strings."""

    def __init__(self):
        self.es_client = Elasticsearch(
            "http://45.13.59.173:9200", http_auth=("elastic", "sicheristsicher"))
        self.index = "tweets"
        self.queue = queue.Queue()

    def get_tweet_list(self, size=100, body={"match_all": {}}):
        """Returns a list of tweet objects of size size."""
        tweets = list()
        response = self.es_client.search(
            index=self.index, size=size, body=body, timeout="1m", request_timeout=30)
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

    def get_queue(self):
        """Return queue object and reset queue."""
        self.queue = queue.Queue()
        return self.queue

    def start_queue(self, batch_size=1000, max_tweets=-1):
        """Start filling queue with tweet texts. Call this after starting worker threads on queue."""

        batch_size = 1000
        body = {
            "query": {
                "match_all": {}
            },
            "size": batch_size,
            "_source": ["text"]
        }
        result = self.es_client.search(index="tweets", body=body, scroll="1m", timeout="1m", request_timeout=30)
        scroll_id = result["_scroll_id"]

        # Put the tweets in the queue and process them
        tweets_loaded = 0
        while True:
            result = self.es_client.scroll(scroll_id=scroll_id, scroll="1m")
            hits = result["hits"]["hits"]

            if len(hits) == 0 or (max_tweets != -1 and tweets_loaded >= max_tweets):
                break

            for doc in hits:
                tweet_text = doc["_source"]["text"]
                self.queue.put(tweet_text)

            tweets_loaded += batch_size
            print(f"Tweets loaded: {tweets_loaded}")
        print("Finished loading all Tweets!")

    def join_queue(self):
        """Joins queue."""
        print("Waiting for queue items to be processed...")
        self.queue.join()
        print("Done")

    def get_client(self):
        """Returns a connection to the elasticsearch server"""
        return self.es_client
