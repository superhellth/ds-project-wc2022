from elasticsearch import Elasticsearch
import tweepy
import twitter_tweet
import elastic_helper

# twitter api access using tweepy client
# working with current permissions
token_file = open('token.txt', 'r')
bearer_token = token_file.readline()
twitter_client = tweepy.Client(bearer_token=bearer_token)

# elasticsearch instancing: 9200 standard port
es_client = Elasticsearch("http://localhost:9200")

# creating an es index if not already existing
index_name = "tweets"
index_exists = es_client.indices.exists(index=index_name)
if not index_exists:
    es_client.index(index=index_name, document=elastic_helper.get_index_structure())


def run_query(query_string, max_results=10):
    tweets = twitter_client.search_recent_tweets(query=search_query, tweet_fields=["id", "author_id", "created_at",
                                                                                   "public_metrics"],
                                                 max_results=max_results)
    # result enumeration and processing
    for tweet_data in tweets.data:
        tweet = twitter_tweet.Tweet(tweet_data)
        user = tweet.author
        tweet.print()

        # send to elasticsearch
        response = es_client.index(
            index=index_name,
            id=tweet.id,
            document=tweet.get_as_es_doc()
        )
        # print(response)


# query definition
search_query = "football #Qatar2022 -is:retweet lang:en"
max_num_tweets = 10
run_query(search_query, max_num_tweets)
