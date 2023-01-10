import threading
from collections import defaultdict
import ujson
import spacy
from middleware.analysis import tweet_provider

class Tokenizer:
    """Custom tokenizer to tokenize tweet texts."""

    def __init__(self, num_threads=4):
        # ES Access
        self.provider = tweet_provider.TweetProvider()

        # tokenization
        self.nlp = spacy.load("en_core_web_sm", disable=["ner", "tagger", "lemmatizer", "parser"])
        self.HASHTAG_SUBSTITUTE = "dswcprojecthashtag"

        # multi-threading
        self.num_threads = num_threads

        # data
        self.counts = defaultdict(int)

    def tokenize(self, text: str):
        """Tokenize Text using custom rules."""
        tokens = []

        text = text.replace("#", self.HASHTAG_SUBSTITUTE)
        doc = self.nlp(text)
        for token in doc:
            if not token.is_punct:
                text = token.lower_.strip().replace(self.HASHTAG_SUBSTITUTE, "#")
                if "http" in token.lower_:
                    text = "<link>"
                if text != '' and text is not None and text and len(text) != 0:
                    tokens.append(text)
        return tokens

    def count_n_grams(self, text: str, n: int):
        """Count n-grams in a document."""
        tokens = self.tokenize(text)
        for i in range(len(tokens) - n):
            n_gram = tuple(tokens[i:i + n])
            self.counts[n_gram] += 1

    def worker(self, queue, processor):
        """Necessary for multi-threading."""
        while True:
            text = queue.get()
            if text is None:
                break
            processor(text)
            queue.task_done()

    def generate_n_grams(self, n: int, write_to: str):
        queue = self.provider.get_queue()
        n_threads = self.num_threads

        # Start the worker threads
        threads = []
        for i in range(n_threads):
            t = threading.Thread(target=lambda: self.worker(queue, lambda text: self.count_n_grams(text, n)))
            t.start()
            threads.append(t)

        self.provider.start_queue(max_tweets=10)
        self.provider.join_queue()

        # Stop the worker threads
        for i in range(n_threads):
            queue.put(None)
        for t in threads:
            t.join()

        with open("./src/data/trigrams.json", "w") as file:
            file.write(ujson.dumps(self.counts))
