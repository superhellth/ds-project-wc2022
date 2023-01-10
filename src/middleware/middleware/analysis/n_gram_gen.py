"""Generates a dict of the tokens in all tweets and their counts. Does not keep cashtags."""
from collections import defaultdict
import threading
import ujson
from middleware.analysis import tweet_provider
from middleware.analysis import nlp_support

provider = tweet_provider.TweetProvider()
tokenizer = nlp_support.Tokenizer()

token_counts = defaultdict(int)

# Multithreading
NUM_THREADS = 3

def process_tweet(tweet_text, word_counts):
    """Count unigrams"""
    for token in tokenizer.tokenize(tweet_text):
        word_counts[token] += 1

def worker():
    while True:
        tweet_text = q.get()
        if tweet_text is None:
            break
        process_tweet(tweet_text, token_counts)
        q.task_done()

q = provider.get_queue()

# Start the worker threads
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

provider.start_queue(max_tweets=10)
print("Waiting for all tweets to be processed...")

# Wait for all the tweets to be processed
provider.join_queue()
print("Done!")

# Stop the worker threads
for i in range(NUM_THREADS):
    q.put(None)
for t in threads:
    t.join()

# write to file

with open("./src/data/trigrams.json", "w") as file:
    file.write(ujson.dumps(token_counts))
