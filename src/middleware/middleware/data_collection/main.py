import sys
import os
from dotenv import load_dotenv
import elasticsearch
import tweepy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.data_collection import elastic_stream_client

### loading env variables ###
print("Trying to read preset environment variables...")
if os.getenv("BEARER_TOKEN") is None:
    print("Error.")
    print("Trying to load local dotenv file...")
    load_dotenv()

try:
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    ES_URL = os.getenv("ES_URL")
    ES_INDEX = os.getenv("ES_INDEX")
    ES_USERNAME = os.getenv("ES_USERNAME")
    ES_PASSWD = os.getenv("ES_PASSWD")
except:
    print("Error.")
    print(
        "You have to provide the following environment variables: BEARER_TOKEN, ES_URL, ES_INDEX, ES_USERNAME, ES_PASSWD either as dotenv file or by setting the manually.")
    sys.exit()

print("Successfully read environment variables!")

# elasticsearch instancing
es_client = elasticsearch.Elasticsearch(ES_URL, http_auth=(ES_USERNAME, ES_PASSWD))

# twitter api access using tweepy client
stream_client = elastic_stream_client.ElasticStreamClient(
    BEARER_TOKEN, es_client, ES_INDEX)

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
                                       "possibly_sensitive", "public_metrics", "referenced_tweets", "reply_settings",
                                       "source", "withheld"],
                         user_fields=["created_at", "description", "entities", "location",
                                      "pinned_tweet_id", "profile_image_url", "protected",
                                      "public_metrics", "url", "verified", "withheld"],
                         expansions="author_id",
                         threaded=True)
    return get_stream_status()


@app.get("/stream/stop")
async def stop_stream():
    """Pauses the stream"""
    stream_client.disconnect()
    return get_stream_status()
