import json
import urllib.parse
import elasticsearch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from file_management import name_is_not_taken

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
    global unigrams_were_loaded
    global sorted_unigrams
    f = open("../../../data/unigrams.json", "r")
    js = json.loads(f.read())
    sorted_unigrams = sorted(js.items(), key=lambda x: x[1], reverse=True)
    unigrams_were_loaded = True


@app.get("/analysis/unigrams/top")
async def get_unigrams(k="100"):
    """Returns top k unigrams"""
    global unigrams_were_loaded
    global sorted_unigrams

    k = int(k)
    if not unigrams_were_loaded: load_unigrams()
    return {entry[0]: entry[1] for entry in sorted_unigrams[:k]}