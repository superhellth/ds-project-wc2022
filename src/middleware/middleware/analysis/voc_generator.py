from middleware.analysis import tweet_provider
from elasticsearch.helpers import scan
from collections import defaultdict
import json
import re
import queue
import threading
import spacy

# ES connection
provider = tweet_provider.TweetProvider()
batch_size = 1000
body = {
    "query": {
        "match_all": {}
    },
    "size": batch_size,
    "_source": ["text"]
}
result = provider.get_client().search(index="tweets", body=body, scroll="1m")
scroll_id = result["_scroll_id"]

# spacy
nlp = spacy.load("en_core_web_sm", disable=["ner", "tagger", "lemmatizer", "parser"])
token_counts = defaultdict(int)

# Multithreading
num_threads = 3

tweets_loaded = 0

def process_tweet(tweet_text, word_counts):
    doc = nlp(tweet_text)
    for token in doc:
        if not token.is_punct:
            text = token.lower_.strip()
            if "http" in token.lower_:
               text = "<link>"
            if text != '' and text is not None and text and len(text) != 0:
                word_counts[text] += 1

def worker():
    while True:
        tweet_text = q.get()
        if tweet_text is None:
            break
        process_tweet(tweet_text, token_counts)
        q.task_done()

q = queue.Queue()

# Start the worker threads
threads = []
for i in range(num_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# Put the tweets in the queue and process them
while True:
    result = provider.get_client().scroll(scroll_id=scroll_id, scroll="1m")
    hits = result["hits"]["hits"]

    if len(hits) == 0:
        break

    for doc in hits:
        tweet_text = doc["_source"]["text"]
        q.put(tweet_text)

    tweets_loaded += batch_size
    print(f"Tweets loaded: {tweets_loaded}")

print("Waiting for all tweets to be processed...")
# Wait for all the tweets to be processed
q.join()
print("Done!")

# Stop the worker threads
for i in range(num_threads):
    q.put(None)
for t in threads:
    t.join()

# write to file
json_str = json.dumps(token_counts)

with open("./src/data/unigrams.json", "w") as file:
    file.write(json_str)

# display top 20 words
# sorted_counts = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)

# for i in range(20):
#     print(sorted_counts[i])