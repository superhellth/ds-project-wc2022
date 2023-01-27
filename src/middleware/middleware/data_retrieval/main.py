from typing import List, Tuple

import elasticsearch
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from middleware.analysis import stat_provider
from middleware.analysis import collocation_graph
from middleware.analysis import tweet_gen
from middleware.analysis import basic_stat_provider
from file_management import get_sentiment_analyzers

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
basic_stat_provider = basic_stat_provider.BasicStatProvider()
graph_generator = collocation_graph.CollocationGraphGenerator(path_to_data_files=PATH_TO_DATA_FILES,
                                                              path_to_graph_files=PATH_TO_GRAPH_FILES)
tweet_generator = tweet_gen.TweetGenerator(provider=stat_provider)


### Providing data from ES ###
@app.get("/query/")
async def get_tweets_that(query: str):
    """Returns all tweets that match the criteria"""
    resp = es_client.search(index=INDEX_NAME, body=query)
    return resp["hits"]["hits"]


@app.get("/statistics/histogram")
async def get_histogram(field, interval, histogram_type):
    """Return all days on between the earliest and latest tweet with corresponding number of tweets"""
    return basic_stat_provider.get_histogram(field, interval, histogram_type)


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
async def get_word_graph(window_size=4, num_edges=50000, include_stop_word_nodes="False", min_node_length=2,
                         embedding_size=128, cluster_alg="agglomerative", n_clusters=11, only_nes="False"):
    """Returns word graph as gexf."""
    window_size = int(window_size)
    num_edges = int(num_edges)
    include_stop_word_nodes = include_stop_word_nodes == "True"
    min_node_length = int(min_node_length)
    embedding_size = int(embedding_size)
    n_clusters = int(n_clusters)
    only_nes = only_nes == "True"
    print(str(only_nes))
    graph_file = graph_generator.generate_and_cluster(window_size=window_size, num_edges=num_edges,
                                                      include_stop_word_nodes=include_stop_word_nodes,
                                                      min_node_length=min_node_length, embedding_size=embedding_size,
                                                      cluster_alg=cluster_alg, n_clusters=n_clusters, only_nes=only_nes)
    return FileResponse(PATH_TO_GRAPH_FILES + graph_file)


### Provide sentiment analysis

@app.post("/analysis/sentiment/tweetsListAvg")
async def get_average_sentiment_for_tweets_list(tweets_text: List[str]):
    """
    Returns the average sentiment of the tweets_text list using all methods available.
    """
    vs, tcs, nbs, berts, = get_sentiment_analyzers()

    return [vs.get_average_sentiment_of_text_list(tweets_text),
            tcs.get_average_sentiment_of_text_list(tweets_text),
            nbs.get_average_sentiment_of_text_list(tweets_text),
            berts.get_average_sentiment_of_text_list(tweets_text)]


@app.get("/analysis/sentiment/tweet")
async def get_sentiment_for_tweet(tweet_text: str):
    """
    Returns the sentiment of the tweets_text list using all methods available.
    """
    vs, tcs, nbs, berts, = get_sentiment_analyzers()

    return [vs.get_sentiment_of_text(tweet_text),
            tcs.get_sentiment_of_text(tweet_text),
            nbs.get_sentiment_of_text(tweet_text),
            berts.get_sentiment_of_text(tweet_text)]


@app.get("/analysis/sentiment/tweetsList")
async def get_sentiment_for_tweets_list(tweets_text: List[str]):
    """
    Returns the sentiment of the tweets_text list using all methods available.
    """
    vs, tcs, nbs, berts, = get_sentiment_analyzers()

    return [vs.get_sentiment_of_text_list(tweets_text),
            tcs.get_sentiment_of_text_list(tweets_text),
            nbs.get_sentiment_of_text_list(tweets_text),
            berts.get_sentiment_of_text_list(tweets_text)]


@app.get("/analysis/sentiment/tweetsListDate")
async def get_sentiment_for_tweets_list_by_date(texts: List[Tuple[str, str]]):
    """
    Returns the sentiment of the text by unique date str.
    """
    vs, tcs, nbs, berts, = get_sentiment_analyzers()

    return [vs.get_sentiment_of_text_list_by_date(texts),
            tcs.get_sentiment_of_text_list_by_date(texts),
            nbs.get_sentiment_of_text_list_by_date(texts),
            berts.get_sentiment_of_text_list_by_date(texts)]
