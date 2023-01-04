import json
import elasticsearch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import spacy

INDEX_NAME = "tweets"

# elasticsearch instancing: 9200 standard port
es_client = elasticsearch.Elasticsearch(
    "http://45.13.59.173:9200", http_auth=("elastic", "sicheristsicher"))

# fastapi instance
app = FastAPI()

# allow access from the following addresses:
origins = [
    "http://localhost:5173/*",
    "http://localhost:5173",
    "http://localhost",
    "http://localhost/",
    "http://176.199.208.10/",
    "http://176.199.208.10"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# spacy
nlp = spacy.load("en_core_web_sm")

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
unigrams_were_loaded = False
sorted_unigrams = None

def load_unigrams():
    """Loads unigrams.json into sorted list of tuples"""
    global unigrams_were_loaded
    global sorted_unigrams
    f = open("../../../data/unigrams.json", "r")
    js = json.loads(f.read())
    sorted_unigrams = sorted(js.items(), key=lambda x: x[1], reverse=True)
    unigrams_were_loaded = True


def get_tokens(k=10, include_stop_words=False, only_hashtags=False, only_mentions=False):
    """Filter unigrams"""
    global unigrams_were_loaded
    global sorted_unigrams
    if not unigrams_were_loaded: load_unigrams()

    result = []
    i = 0
    j = 0
    while i < k:
        token = sorted_unigrams[j][0]
        if include_stop_words or token not in nlp.Defaults.stop_words:
            if not only_hashtags or (only_hashtags and token[0] == "#"):
                if not only_mentions or (only_mentions and token[0] == "@"):
                    result.append(sorted_unigrams[j])
                    i += 1
        j += 1
    
    return {entry[0]: entry[1] for entry in result}


@app.get("/analysis/unigrams/top")
async def get_unigrams(k="10", include_stop_words="False", only_mentions="False", only_hashtags="False"):
    """Returns top k unigrams"""

    k = int(k)
    include_stop_words = include_stop_words == "True"
    only_mentions = only_mentions == "True"
    only_hashtags = only_hashtags == "True"

    return get_tokens(k=k, include_stop_words=include_stop_words, only_mentions=only_mentions, only_hashtags=only_hashtags)
