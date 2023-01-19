import multiprocessing
from collections import defaultdict
import spacy
from middleware.analysis import tweet_provider
from middleware.analysis.multithreading import MultiThreading


class CorpusAnalyzer:
    """Analyzer to generate n-gram- and collocation-counts."""

    def __init__(self):
        self.provider = tweet_provider.TweetProvider()

        # tokenization
        self.nlp = spacy.load("en_core_web_sm", disable=["ner", "tagger", "lemmatizer", "parser"])
        self.HASHTAG_SUBSTITUTE = "dswcprojecthashtag"

        # multi-threading
        self.multi_threading = MultiThreading()

        # data
        self.counts = None
        self.tokenized_tweets = []
        self.queue = self.provider.get_queue()

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

    def count_collocations(self, text: str, window_size: int):
        """Count collocations in a document."""
        tokens = self.tokenize(text)
        for i in range(len(tokens) - 1):
            for j in range(i + 1, min(len(tokens), i + window_size)):
                collocation_list = sorted([tokens[i], tokens[j]])
                collocation = (collocation_list[0], collocation_list[1])
                self.counts[collocation] += 1

    def new_tokenize(self, text: str):
        # Replace '#' with a substitute character to prevent issues with tokenizing hashtags
        text = text.replace("#", self.HASHTAG_SUBSTITUTE)

        # Remove all non-ASCII characters
        text = "".join(c for c in text if ord(c) < 128)

        # Remove special characters which are not alphanumeric or whitespace
        text = "".join(c for c in text if c.isalnum() or c.isspace())

        # Tokenize the text
        doc = self.nlp(text)

        # Remove stop words and punctuation
        tokens = [token.lower_ for token in doc if not token.is_stop or not token.is_punct]

        # Replace tokens that contain "http" with "<link>"
        tokens = ["<link>" if "http" in token else token for token in tokens]

        # Replace the substitute character with '#'
        tokens = [token.replace(self.HASHTAG_SUBSTITUTE, "#") for token in tokens]

        # Remove new lines
        tokens = [token if token != "\n" else "" for token in tokens]

        # Remove empty or fields that contain new lines
        tokens = [token for token in tokens if token.strip() and '\n' not in token]

        # Remove any token of length less than 1
        tokens = [token for token in tokens if len(token) > 1]

        return tokens

    def tokenize_tweet(self, text: str):
        """Tokenizes a tweet and append it to class attribute."""
        tokens = self.new_tokenize(text)
        self.tokenized_tweets.append(tokens)

    def execute_task(self, task, num_threads, batch_size, num_tweets):
        """Execute the given task with the given number of threads."""
        self.queue = self.provider.get_queue()
        self.counts = defaultdict(int)

        # Start the worker threads
        self.multi_threading.start_threads(task, self.queue, num_threads)
        # Start feeding queue
        self.provider.start_queue(batch_size=batch_size, max_tweets=num_tweets)
        # Finish for all queue items to be processed
        self.provider.join_queue()
        # Stop the worker threads
        self.multi_threading.stop_threads(self.queue)

    def generate_n_grams(self, n, batch_size=1000, num_tweets=-1, num_threads=4):
        """Generate n-grams from the corpus."""
        print("Start generating n-grams...")
        self.execute_task(lambda text: self.count_n_grams(text, n), num_threads, batch_size, num_tweets)
        print()
        return self.counts

    def generate_collocation_counts(self, window_size, batch_size=1000, num_tweets=-1, num_threads=4):
        """Generate collocation counts from the corpus."""
        print("Start generating collocation counts...")
        self.execute_task(lambda text: self.count_collocations(text, window_size), num_threads, batch_size, num_tweets)
        print()
        return self.counts

    def generate_tokenized_tweets(self, batch_size=1000, num_tweets=-1, num_threads=multiprocessing.cpu_count()):
        """Generate tokenized tweets"""
        print("Start generating tokenized tweets")
        self.execute_task(lambda text: self.tokenize_tweet(text), num_threads, batch_size, num_tweets)
        print()
        return self.tokenized_tweets
