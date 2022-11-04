import elasticsearch
import tweepy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import elastic_stream_client

# twitter api access using tweepy client
# working with current permissions
token_file = open('../twitter-api-bearer-token.txt', 'r', encoding="utf_8")
bearer_token = token_file.readline()
INDEX_NAME = "tweets"

# elasticsearch instancing: 9200 standard port
es_client = elasticsearch.Elasticsearch("http://45.13.59.173:9200")
stream_client = elastic_stream_client.ElasticStreamClient(
    bearer_token, es_client, INDEX_NAME)

# fastapi instance
app = FastAPI()

# allow access from the following addresses:
origins = [
    "http://localhost:5173/",
    "http://localhost:5173",
    "http://localhost",
    "http://localhost/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_stream_status():
    """Returns the status of the stream. Including running state and rule"""
    rule = "Invalid"
    rule_data = stream_client.get_rules().data
    if rule_data is not None:
        rule = stream_client.get_rules().data[0][0].replace("hashtag", "#")
    return {
        "running": stream_client.running,
        "rule": rule
    }


@app.get("/query/")
async def get_tweets():
    """Returns all tweets from the connected elasticsearch instance"""
    resp = es_client.search(index="tweets")
    return resp["hits"]["hits"]


@app.get("/stream/setRule")
async def set_rule(rule: str):
    """Updates the rule of the stream"""
    # Necessary because "#" can't be part of the url
    rule = rule.replace("hashtag", "#")
    rule_data = stream_client.get_rules().data
    if rule_data is not None:
        for a_rule in rule_data:
            stream_client.delete_rules(a_rule[2])

    stream_client.add_rules(tweepy.StreamRule(rule))

    return get_stream_status()


@app.get("/stream/status")
async def stream_status():
    """Returns the status of the stream. Including running state and rule"""
    return get_stream_status()


@app.get("/stream/start")
async def start_stream():
    """Starts the stream"""
    stream_client.filter(tweet_fields=["attachments", "author_id", "context_annotations", "conversation_id",
                                       "created_at", "edit_controls", "entities", "in_reply_to_user_id", "lang",
                                       "possibly_sensitive", "public_metrics", "referenced_tweets", "reply_settings", "source", "withheld"], threaded=True)
    return get_stream_status()


@app.get("/stream/stop")
async def stop_stream():
    """Pauses the stream"""
    stream_client.disconnect()
    return get_stream_status()
