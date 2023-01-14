import elasticsearch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.analysis import stat_provider

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
stat_provider = stat_provider.StatProvider(path_to_data_files="../../../data/")

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

    return stat_provider.get_top_unigrams(k=k, include_stop_words=include_stop_words, only_mentions=only_mentions, only_hashtags=only_hashtags)

@app.get("/analysis/ngrams/top")
async def get_n_grams(n, k="10"):
    """Returns top k n-grams."""
    
    n = int(n)
    k = int(k)

    return stat_provider.get_top_n_grams(n, k)
