import os
import sys
import queue
from dotenv import load_dotenv
from elasticsearch import helpers, Elasticsearch
from middleware.tweet_management import twitter_tweet


class TweetProvider:
    """This class provides tweets from ES either as tweet objects or as strings."""

    def __init__(self):
        print("Trying to read preset environment variables...")
        if os.getenv("ES_URL") is None:
            print("Error.")
            print("Trying to load local dotenv file...")
            load_dotenv()

        try:
            es_url = os.getenv("ES_URL")
            es_index = os.getenv("ES_INDEX")
            es_username = os.getenv("ES_USERNAME")
            es_passwd = os.getenv("ES_PASSWD")
        except:
            print("Error.")
            print(
                "You have to provide the following environment variables: PATH_TO_DATA_FILES, ES_URL, ES_INDEX, ES_USERNAME, ES_PASSWD either as dotenv file or by setting the manually.")
            sys.exit()

        print("Successfully read environment variables!")

        self.es_client = Elasticsearch(
            es_url, http_auth=(es_username, es_passwd))
        self.index = es_index
        self.queue = queue.Queue()

    def get_tweet_list(self, size=100, body={"match_all": {}}):
        """Query the elasticsearch index.

        Args:
            size (int, optional): Number of results to return. Defaults to 100.
            body (dict, optional): Body of the query. Defaults to {"match_all": {}}.

        Returns:
            list: List of Tweet object matching the query.
        """
        tweets = list()
        response = self.es_client.search(
            index=self.index, size=size, body=body, timeout="1m", request_timeout=30)
        for tweet in response["hits"]["hits"]:
            tweets.append(twitter_tweet.Tweet(tweet, is_es_doc=True))
        return tweets

    def get_corpus(self, size=100, body=None):
        """Returns a list of strings of size size.

        Args:
            size (int, optional): Number of tweet texts to return. Defaults to 100.
            body (dict, optional): Body of the query. Defaults to None.

        Returns:
            list: List of tweet texts as string.
        """
        corpus = list()
        for document in helpers.scan(self.es_client, index=self.index, _source=["text"], body=body):
            corpus.append(document["_source"]["text"])
            if len(corpus) == size:
                break
        return corpus

    def get_queue(self):
        """Return queue object and reset queue.

        Returns:
            queue: Queue object which will be feeded with tweet texts, as soon as start_queue is called.
        """
        self.queue = queue.Queue()
        return self.queue

    def start_queue(self, batch_size=1000, max_tweets=-1):
        """Start filling queue with tweet texts. Call this after starting worker threads on queue.

        Args:
            batch_size (int, optional): Number of tweets to be queried per request from the es index. Defaults to 1000.
            max_tweets (int, optional): Number of tweet texts to put into the queue. Always rounded up to a multiple of batch_size.
            When -1 uses whole corpus. Defaults to -1.
        """

        batch_size = 1000
        body = {
            "query": {
                "match_all": {}
            },
            "size": batch_size,
            "_source": ["text"]
        }
        result = self.es_client.search(index="tweets", body=body, scroll="1m", request_timeout=30)
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
        """Returns a connection to the elasticsearch server.

        Returns:
            Elasticsearch: Instance of the providers connection to elasticsearch.
        """
        return self.es_client
