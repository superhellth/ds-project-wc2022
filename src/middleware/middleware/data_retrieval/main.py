from typing import List, Tuple

import elasticsearch
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from middleware.analysis import stat_provider
from middleware.analysis import collocation_graph
from middleware.analysis import tweet_gen
from middleware.analysis.sentiment_vaderSentiment import VaderSentiment
from middleware.analysis.sentiment_trained_classifier import TrainedClassifierSentiment

INDEX_NAME = "tweets"

# elasticsearch instancing: 9200 standard port
es_client = elasticsearch.Elasticsearch(
    "http://45.13.59.173:9200", http_auth=("elastic", "sicheristsicher"))

# fastapi instance
app = FastAPI()

# allow access from the following addresses:
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# fetch local data
PATH_TO_DATA_FILES = "../../../data/"
PATH_TO_GRAPH_FILES = "../../../data/word-graph/"
stat_provider = stat_provider.StatProvider(path_to_data_files=PATH_TO_DATA_FILES)
graph_generator = collocation_graph.CollocationGraphGenerator(path_to_data_files=PATH_TO_DATA_FILES,
                                                              path_to_graph_files=PATH_TO_GRAPH_FILES)
tweet_generator = tweet_gen.TweetGenerator(provider=stat_provider)


### Providing data from ES ###
@app.get("/query/")
async def get_tweets_that(query: str):
    """Returns all tweets that match the criteria"""
    resp = es_client.search(index=INDEX_NAME, body=query)
    return resp["hits"]["hits"]


@app.get("/statistics/tweetsPerDay")
async def get_tweet_number_by_days():
    """Return all days on between the earliest and latest tweet with corresponding number of tweets"""
    resp = es_client.search(index=INDEX_NAME, body={
        "size": 0,
        "aggs": {
            "tweets_per_day": {
                "date_histogram": {
                    "field": "created_at",
                    "interval": "day"
                }
            }
        }
    })

    # Access the dates and aggregated numbers from the response
    buckets = resp['aggregations']['tweets_per_day']['buckets']
    date_dict = dict()
    for bucket in buckets:
        date = bucket['key_as_string']
        count = bucket['doc_count']
        date_dict[date] = count
    return date_dict


@app.get("/validate")
async def validate_query(query: str = "false"):
    """Validates the given query"""
    resp = es_client.indices.validate_query(index=INDEX_NAME, body=query, explain=True)
    return resp


### Providing data from local files ###
@app.get("/analysis/unigrams/top")
async def get_unigrams(k="10", include_stop_words="False", only_mentions="False", only_hashtags="False"):
    """Returns top k unigrams."""

    k = int(k)
    include_stop_words = include_stop_words == "True"
    only_mentions = only_mentions == "True"
    only_hashtags = only_hashtags == "True"

    return stat_provider.get_top_unigrams(k=k, include_stop_words=include_stop_words, only_mentions=only_mentions,
                                          only_hashtags=only_hashtags)


@app.get("/analysis/ngrams/top")
async def get_n_grams(n, k="10"):
    """Returns top k n-grams."""

    n = int(n)
    k = int(k)

    return stat_provider.get_top_n_grams(n, k)


@app.get("/analysis/ngrams/generateTweet")
async def generate_tweet_from_n_grams(given, tweet_length, n, percent_n_grams, allow_repitition):
    tweet_length = int(tweet_length)
    n = int(n)
    percent_n_grams = float(percent_n_grams)
    allow_repitition = allow_repitition == "True"
    return tweet_generator.gen_tweet_from(given, tweet_length, n, percent_n_grams, allow_repitition)


@app.get("/analysis/graph")
async def get_word_graph(window_size=4, num_edges=50000, include_stop_word_nodes=False, min_node_length=2,
                         embedding_size=128, cluster_alg="agglomerative", n_clusters=11):
    """Returns word graph as gexf."""
    window_size = int(window_size)
    num_edges = int(num_edges)
    include_stop_word_nodes = include_stop_word_nodes == "True"
    min_node_length = int(min_node_length)
    embedding_size = int(embedding_size)
    n_clusters = int(n_clusters)
    graph_file = graph_generator.generate_and_cluster(window_size=window_size, num_edges=num_edges,
                                                      include_stop_word_nodes=include_stop_word_nodes,
                                                      min_node_length=min_node_length, embedding_size=embedding_size,
                                                      cluster_alg=cluster_alg, n_clusters=n_clusters)
    return FileResponse(PATH_TO_GRAPH_FILES + graph_file)


### Provide sentiment analysis

@app.get("/analysis/sentiment/tweetsListAvg")
async def get_average_sentiment_for_tweets_list(tweets_text: List[str]):
    """
    Returns the average sentiment of the tweets_text list using all methods available.
    """

    v = VaderSentiment("vaderSent")
    c = TrainedClassifierSentiment("trainedClassSent")
    return [v.get_average_sentiment_of_text_list(tweets_text),
            c.get_average_sentiment_of_text_list(tweets_text)]


@app.get("/analysis/sentiment/tweet")
async def get_sentiment_for_tweet(tweet_text: str):
    """
    Returns the sentiment of the tweets_text list using all methods available.
    """
    v = VaderSentiment("vaderSent")
    c = TrainedClassifierSentiment("trainedClassSent")

    return [v.get_sentiment_of_text(tweet_text),
            c.get_sentiment_of_text(tweet_text)]


@app.get("/analysis/sentiment/tweetsList")
async def get_sentiment_for_tweets_list(tweets_text: List[str]):
    """
    Returns the sentiment of the tweets_text list using all methods available.
    """

    v = VaderSentiment("vaderSent")
    c = TrainedClassifierSentiment("trainedClassSent")
    return [v.get_sentiment_of_text_list(tweets_text),
            c.get_sentiment_of_text_list(tweets_text)]


@app.get("/analysis/sentiment/tweetsListDate")
async def get_sentiment_for_tweets_list_by_date(texts: List[Tuple[str, str]]):
    """
    Returns the sentiment of the text by unique date str.
    """

    v = VaderSentiment("vaderSent")
    c = TrainedClassifierSentiment("trainedClassSent")
    return [v.get_sentiment_of_text_list_by_date(texts),
            c.get_sentiment_of_text_list_by_date(texts)]
