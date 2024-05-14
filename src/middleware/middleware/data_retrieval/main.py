import sys
from dotenv import load_dotenv
import json
import os.path
from typing import List, Tuple
import matplotlib.pyplot as plt
import ujson
import elasticsearch
from gensim.models import Word2Vec
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from middleware.analysis import stat_provider
from middleware.analysis import collocation_graph
from middleware.analysis import basic_stat_provider
from middleware.analysis import embedding
from middleware.data_retrieval.file_management import get_sentiment_analyzers

### loading env variables ###
print("Trying to read preset environment variables...")
if os.getenv("PATH_TO_DATA_FILES") is None:
    print("Error.")
    print("Trying to load local dotenv file...")
    load_dotenv()

try:
    PATH_TO_DATA_FILES = os.getenv("PATH_TO_DATA_FILES")
    ES_URL = os.getenv("ES_URL")
    ES_INDEX = os.getenv("ES_INDEX")
    ES_USERNAME = os.getenv("ES_USERNAME")
    ES_PASSWD = os.getenv("ES_PASSWD")
except:
    print("Error.")
    print(
        "You have to provide the following environment variables: PATH_TO_DATA_FILES, ES_URL, ES_INDEX, ES_USERNAME, ES_PASSWD either as dotenv file or by setting the manually.")
    sys.exit()

print("Successfully read environment variables!")
print(f"Reading data from: {PATH_TO_DATA_FILES}")

## path to data files
# Bastian: /Users/bastianmuller/Desktop/Studium/Informatik_HD/7_HWS22:23/INF_ITA/Project/code/src/data/
# Nico: ../../../data/
PATH_TO_GRAPH_FILES = PATH_TO_DATA_FILES + "word-graph/"
PATH_TO_SENTIMENT_MODELS = PATH_TO_DATA_FILES + "sentiment-models/"
PATH_TO_SENTIMENT_DATA = PATH_TO_DATA_FILES + "sentiment-data/"
PATH_TO_EMBEDDING_DATA = PATH_TO_DATA_FILES + "word-embeddings/"
PATH_TO_OTHER_TRAINING_DATA = PATH_TO_SENTIMENT_DATA + "Tweets_train.csv"
PATH_TO_WORD2VEC_MODEL = PATH_TO_EMBEDDING_DATA + "w2v_epochs=100.emb"
PATH_TO_OTHER_VALIDATION_DATA = PATH_TO_SENTIMENT_DATA + "Tweets_test.csv"
PATH_TO_OWN_TRAINING_DATA = PATH_TO_SENTIMENT_DATA + "classification_with_text_train.csv"
PATH_TO_OWN_VALIDATION_DATA = PATH_TO_SENTIMENT_DATA + "classification_with_text_test.csv"

## loading options
LOAD_N_GRAMS_ON_STARTUP = False

## elasticsearch connection
INDEX_NAME = ES_INDEX
es_client = elasticsearch.Elasticsearch(
    ES_URL, http_auth=(ES_USERNAME, ES_PASSWD), use_ssl=True, verify_certs=False, ssl_show_warn=False)

## fastapi config
app = FastAPI()
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

### Loading data on startup ###
## n-grams
print("Preparing n-gram data...")
stat_provider = stat_provider.StatProvider(path_to_data_files=PATH_TO_DATA_FILES)
if LOAD_N_GRAMS_ON_STARTUP:
    print("Loading n-grams from file...")
    stat_provider.load_n_grams(2)
    stat_provider.load_n_grams(3)
    stat_provider.load_n_grams(4)

## utility
print("Loading utility classes...")
basic_stat_provider = basic_stat_provider.BasicStatProvider()

## collocation graph
print("Loading collocation graph generator...")
graph_generator = collocation_graph.CollocationGraphGenerator(path_to_data_files=PATH_TO_DATA_FILES,
                                                              path_to_graph_files=PATH_TO_GRAPH_FILES)

## sentiment analysis
# create sentiment-models folder in data dir if it does not exist
if not os.path.exists(PATH_TO_SENTIMENT_MODELS):
    print("Creating 'data/sentiment-models' dir...")
    os.makedirs(PATH_TO_SENTIMENT_MODELS)

# load models
print("Loading sentiment models...")
vs, lrcother, lrcown, berts = get_sentiment_analyzers(PATH_TO_SENTIMENT_MODELS, PATH_TO_OTHER_TRAINING_DATA,
                                                      PATH_TO_OTHER_VALIDATION_DATA, PATH_TO_OWN_TRAINING_DATA,
                                                      PATH_TO_OWN_VALIDATION_DATA)

## word embeddings
print("Loading word embedding model...")
w2v_model = Word2Vec.load(PATH_TO_WORD2VEC_MODEL)
embedder = embedding.Embedder(PATH_TO_DATA_FILES, PATH_TO_EMBEDDING_DATA)


### Provide data from ES ###
@app.get("/query/raw")
async def query_raw(query: str):
    resp = es_client.search(index=INDEX_NAME, body=query, timeout="2m", request_timeout=60)
    return resp


@app.get("/query/")
async def get_tweets_that(query: str):
    """Returns all tweets that match the criteria"""
    resp = es_client.search(index=INDEX_NAME, body=query)
    js = ujson.loads(query)
    return {"hits": resp["hits"]["hits"], "counts": basic_stat_provider.get_number_of_tweets(query=js["query"])}


@app.get("/statistics/histogram")
async def get_histogram(field, interval, histogram_type):
    """Return all days on between the earliest and latest tweet with corresponding number of tweets"""
    return basic_stat_provider.get_histogram(field, interval, histogram_type)


@app.get("/validate")
async def validate_query(query: str = "false"):
    """Validates the given query"""
    resp = es_client.indices.validate_query(index=INDEX_NAME, body=query, explain=True)
    return resp


### Provide data from local files ###
## n-grams
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


## colloction graph
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
    graph_file = graph_generator.generate_and_cluster(window_size=window_size, num_edges=num_edges,
                                                      include_stop_word_nodes=include_stop_word_nodes,
                                                      min_node_length=min_node_length, embedding_size=embedding_size,
                                                      cluster_alg=cluster_alg, n_clusters=n_clusters, only_nes=only_nes)
    return FileResponse(PATH_TO_GRAPH_FILES + graph_file)


## sentiment analysis
@app.post("/analysis/sentiment/tweetsListAvg")
async def get_average_sentiment_for_tweets_list(tweets_text: List[str]):
    """
    Returns the average sentiment of the tweets_text list using all methods available.
    """
    return [vs.get_average_sentiment_of_text_list(tweets_text),
            lrcother.get_average_sentiment_of_text_list(tweets_text),
            lrcown.get_average_sentiment_of_text_list(tweets_text),
            berts.get_average_sentiment_of_text_list(tweets_text)]


@app.post("/analysis/sentiment/tweet")
async def get_sentiment_for_tweet(tweet_text: dict):
    """
    Returns the sentiment of the tweets_text list using all methods available.
    """
    tweet_text = list(tweet_text.values())[0]
    return [vs.get_sentiment_of_text(tweet_text),
            lrcother.get_sentiment_of_text(tweet_text),
            lrcown.get_sentiment_of_text(tweet_text),
            berts.get_sentiment_of_text(tweet_text)]


@app.get("/analysis/sentiment/tweetsList")
async def get_sentiment_for_tweets_list(tweets_text: List[str]):
    """
    Returns the sentiment of the tweets_text list using all methods available.
    """
    return [vs.get_sentiment_of_text_list(tweets_text),
            lrcother.get_sentiment_of_text_list(tweets_text),
            lrcown.get_sentiment_of_text_list(tweets_text),
            berts.get_sentiment_of_text_list(tweets_text)]


@app.get("/analysis/sentiment/tweetsListDate")
async def get_sentiment_for_tweets_list_by_date(texts: List[Tuple[str, str]]):
    """
    Returns the sentiment of the text by unique date str.
    """
    return [vs.get_sentiment_of_text_list_by_date(texts),
            lrcother.get_sentiment_of_text_list_by_date(texts),
            lrcown.get_sentiment_of_text_list_by_date(texts),
            berts.get_sentiment_of_text_list_by_date(texts)]


@app.get("/analysis/sentiment/meanSentiment")
async def get_mean_overall_sentiment():
    """
    Returns the mean overall sentiment calculated by all methods.
    """
    with open(PATH_TO_SENTIMENT_DATA + 'mean_sentiment.json') as f:
        data = json.load(f)
    return data


@app.get("/analysis/sentiment/sentimentOverTime")
async def get_sentiment_over_time():
    """
    Returns the dictionary that contains the sentiment values over time.
    """
    with open(PATH_TO_SENTIMENT_DATA + 'sentiment_over_time.json') as f:
        data = json.load(f)
    return data


@app.get("/analysis/sentiment/trainedModelPerformance")
async def get_trained_model_performance():
    """
    Returns the accuracy, recall and f1 score of the two trained models
    """
    return [lrcother.accuracy(), lrcother.recall(), lrcother.f1_score(),
            lrcown.accuracy(), lrcown.recall(), lrcown.f1_score()]


@app.get("/analysis/sentiment/sentimentByCategory")
async def get_sentiment_by_category():
    """
    Returns the dictionary that contains the sentiment values by category.
    """
    with open(PATH_TO_SENTIMENT_DATA + 'category_sent.json') as f:
        data = json.load(f)
    return data


@app.get("/analysis/sentiment/qatarSentiment")
async def get_qatar_sentiment():
    """
    Returns the sentiment of tweets that mention 'qatar' over time
    """
    with open(PATH_TO_SENTIMENT_DATA + 'qatar_sentiment.json') as f:
        data = json.load(f)
    return data


## word embedding
@app.get("/analysis/embedding/exists")
async def word_in_w2v_vocab(word: str):
    """Check for existing Word2Vec Embedding for a word."""
    return word in w2v_model.wv.key_to_index.keys()


@app.get("/analysis/embedding/similar")
async def get_similar(positive: List[str] = Query(default=None), negative: List[str] = Query(default=None),
                      k: int = 10):
    """Get similar words."""
    return {"similar": w2v_model.wv.most_similar(positive=positive, negative=negative, topn=k)}


@app.get("/analysis/embedding/doesntmatch")
async def doesnt_match(word: List[str] = Query(default=None)):
    """Find word that doesn't match."""
    return w2v_model.wv.doesnt_match(word)


@app.get("/analysis/embedding/tsne")
async def get_tsne(word: str, num_closest: str = "10", num_furthest: str = "0", file_prefix: str = "1"):
    """Return TSNE plot of word."""
    embedder.tsneplot(w2v_model, word, num_closest=int(num_closest), num_furthest=int(num_furthest))
    path_to_file = PATH_TO_EMBEDDING_DATA + file_prefix + "-tsne.png"
    plt.savefig(path_to_file, format="png")
    return FileResponse(path_to_file)


@app.get("/analysis/embedding/distance")
async def get_relative_distance(word1: str, word2: str):
    return w2v_model.wv.distance(word1, word2)
