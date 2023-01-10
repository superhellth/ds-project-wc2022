"""Script to build collocation graph."""

import threading
from collections import defaultdict
import ujson
import spacy
from middleware.analysis import tweet_provider

provider = tweet_provider.TweetProvider()
nlp = spacy.load("en_core_web_sm", disable=["ner", "tagger", "lemmatizer", "parser"])
PLACEHOLDER_STRING = "dswcproject"
NUM_THREADS = 10
collocations = defaultdict(int)
WINDOW_SIZE = 3 # change file at the bottom if you change this number, otherwise the old file will be overwritten

def process_tweet(tweet_text, collocations, window_size=2):
    tweet_text = tweet_text.replace("#", PLACEHOLDER_STRING)
    doc = nlp(tweet_text)
    token_list = []
    for token in doc:
        if not token.is_punct:
            text = token.lower_.strip().replace(PLACEHOLDER_STRING, "#")
            if "http" in token.lower_:
                text = "<link>"
            if text != '' and text is not None and text and len(text) != 0:
                token_list.append(text)
    for i in range(len(token_list) - 1):
        for j in range(i + 1, min(len(token_list), i + window_size)):
            collocation = (token_list[i], token_list[j])
            collocations[collocation] += 1

q = provider.get_queue()

def worker():
    while True:
        tweet_text = q.get()
        if tweet_text is None:
            break
        process_tweet(tweet_text, collocations, window_size=WINDOW_SIZE)
        q.task_done()

# Start the worker threads
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

provider.start_queue()
provider.join_queue()

# Stop the worker threads
for i in range(NUM_THREADS):
    q.put(None)
for t in threads:
    t.join()

with open("./src/data/collocations3.json", "w") as file:
    file.write(ujson.dumps(collocations))
