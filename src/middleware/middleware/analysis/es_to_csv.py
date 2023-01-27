from elasticsearch import Elasticsearch
import pandas as pd
from middleware.tweet_management import twitter_tweet

es_client = Elasticsearch(
            "http://45.13.59.173:9200", http_auth=("elastic", "sicheristsicher"))
INDEX = "tweets"
FIELDS = ["author.created_at", "author.description", "author.id", "author.location", "author.name", "author.pinned_tweet_id", "author.profile_image_url", "author.public_metrics.followers_count", "author.public_metrics.following_count", "author.public_metrics.listed_count", "author.public_metrics.tweet_count", "author.url", "author.username", "author.verified", "conversation_id", "created_at", "edit_history_tweet_ids", "id", "in_reply_to_user_id", "lang", "possibly_sensitive", "public_metrics.like_count", "public_metrics.quote_count", "public_metrics.reply_count", "public_metrics.retweet_count", "reply_settings", "source", "text"]
MAX_TWEETS = -1
BATCH_SIZE = 1000
BODY = {
    "query": {
        "match_all": {}
    },
    "size": BATCH_SIZE,
    "_source": FIELDS
}
df = pd.DataFrame(columns=FIELDS)
result = es_client.search(index="tweets", body=BODY, scroll="3m", timeout="1m", request_timeout=30)
scroll_id = result["_scroll_id"]

# Put the tweets in the queue and process them
tweets_loaded = 0
while True:
    hits = result["hits"]["hits"]

    if len(hits) == 0 or (MAX_TWEETS != -1 and tweets_loaded >= MAX_TWEETS):
        break

    for doc in hits:
        doc = pd.json_normalize(doc)
        # if "\n" in doc["_source.text"][0]:
        #     print(repr(doc["_source.text"][0]))
        last_index = df.last_valid_index()
        if last_index is None:
            last_index = 0
        else:
            last_index = last_index + 1
        df.loc[last_index] = pd.Series(
            {field: repr(doc["_source." + field][0]) for field in FIELDS})
    df.to_csv("./src/data/index.csv", sep=",",
                    columns=FIELDS, index=False, lineterminator="\n")

    tweets_loaded += BATCH_SIZE
    print(f"Tweets loaded: {tweets_loaded}")
    result = es_client.scroll(scroll_id=scroll_id, scroll="1m")
