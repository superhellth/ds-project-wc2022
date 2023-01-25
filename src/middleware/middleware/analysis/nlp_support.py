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
        self.nlp = spacy.load("en_core_web_sm", disable=[
                              "ner", "tagger", "lemmatizer", "parser"])
        self.ner_nlp = spacy.load("en_core_web_sm", disable=["lemmatizer"])
        self.HASHTAG_SUBSTITUTE = "dswcprojecthashtag"

        # multi-threading
        self.multi_threading = MultiThreading()

        # data
        self.counts = None
        self.tokenized_tweets = []
        self.queue = self.provider.get_queue()

    def tokenize(self, text: str, use_advanced_tokenize: bool = False):
        """Tokenize Text using custom rules.

        Args:
            text (str): String to tokenize.
            use_advanced_tokenize (bool, optional): If True the tokenizer removes stop words, non-ASCII characters and special characters.
            Also removes tokens of size 1. Defaults to False.

        Returns:
            list: List of tokens.
        """
        tokens = []
        text = text.replace("#", self.HASHTAG_SUBSTITUTE)

        if use_advanced_tokenize:
            # Remove all non-ASCII characters
            text = "".join(c for c in text if ord(c) < 128)
            # Remove special characters which are not alphanumeric or whitespace
            text = "".join(c for c in text if c.isalnum() or c.isspace())

        doc = self.nlp(text)

        if use_advanced_tokenize:
            # Remove stop words and punctuation
            tokens = [
                token.lower_ for token in doc if not token.is_stop and not token.is_punct]
        else:
            for token in doc:
                if not token.is_punct:
                    text = token.lower_.strip().replace(self.HASHTAG_SUBSTITUTE, "#")
                    if "http" in token.lower_:
                        text = "<link>"
                    if text != '' and text is not None and text and len(text) != 0:
                        tokens.append(text)

        if use_advanced_tokenize:
            # Replace tokens that contain "http" with "<link>"
            tokens = ["<link>" if "http" in token else token for token in tokens]
            # Replace the substitute character with '#'
            tokens = [token.replace(self.HASHTAG_SUBSTITUTE, "#")
                      for token in tokens]
            # Remove new lines
            tokens = [token if token != "\n" else "" for token in tokens]

        # Remove empty or fields that contain new lines
        tokens = [token for token in tokens if token.strip()
                  and '\n' not in token]
        # Remove any token of length less than 1
        tokens = [token for token in tokens if len(token) > 1]

        return tokens

    def count_n_grams(self, text: str, n: int):
        """Count n-grams in a document.

        Args:
            text (str): document of which to count n-grams.
            n (int): n-gram size.
        """
        tokens = self.tokenize(text)
        for i in range(len(tokens) - n):
            n_gram = tuple(tokens[i:i + n])
            self.counts[n_gram] += 1

    def count_collocations(self, text: str, window_size: int):
        """Count collocations in a document.

        Args:
            text (str): document of which to count collocations.
            window_size (int): window size of collocations.
        """
        tokens = self.tokenize(text)
        for i in range(len(tokens) - 1):
            for j in range(i + 1, min(len(tokens), i + window_size)):
                collocation_list = sorted([tokens[i], tokens[j]])
                collocation = (collocation_list[0], collocation_list[1])
                self.counts[collocation] += 1

    def tokenize_tweet(self, text: str):
        """Tokenizes a tweet and append it to class attribute tokenized_tweets.

        Args:
            text (str): document to tokenize.
        """
        tokens = self.tokenize(text)
        self.tokenized_tweets.append(tokens)

    def count_nes_collocations(self, text: str):
        """Count the cooccurences of named entities.

        Args:
            text (str): document to analyze.
        """
        doc = self.ner_nlp(text)
        for i in range(len(doc.ents) - 1):
            for j in range(i + 1, len(doc.ents)):
                ent1 = doc.ents[i].text
                ent2 = doc.ents[j].text
                if ent1 != ent2:
                    ent1 = "".join(c for c in ent1 if ord(c) < 128)
                    ent1 = "".join(c for c in ent1 if c.isalnum() or c.isspace()).replace("#", "").strip().lower()
                    ent2 = "".join(c for c in ent2 if ord(c) < 128)
                    ent2 = "".join(c for c in ent2 if c.isalnum() or c.isspace()).replace("#", "").strip().lower()
                    if ent1 != "" and ent2 != "" and "http" not in ent1 and "http" not in ent2:
                        collocation_list = sorted([ent1, ent2])
                        collocation = (collocation_list[0], collocation_list[1])
                        self.counts[collocation] += 1

    def count_nes(self, text: str):
        """Count the appearance of named entities.

        Args:
            text (str): document to analyze.
        """
        doc = self.ner_nlp(text)
        for ent in doc.ents:
            self.counts[(ent.text, ent.label_)] += 1

    def execute_task(self, task, num_threads, batch_size, num_tweets):
        """Execute the given task with the given number of threads.

        Args:
            task (function): Function to execute on the worker threads.
            num_threads (int): Number of threads to execute the task on.
            batch_size (int): Number of tweets to load at once from es.
            num_tweets (int): Number of tweets to execute the task on. Always rounded up to a multiple of batch_size. When -1 uses whole corpus.
        """
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

    def generate_n_grams(self, n, batch_size=1000, num_tweets=-1, num_threads=multiprocessing.cpu_count()):
        """Generate n-grams from the corpus.

        Args:
            n (int): n-gram size.
            batch_size (int, optional): Number of tweets to load at once from es. Defaults to 1000.
            num_tweets (int, optional): Number of tweets to use for the n-gram generation. When -1 uses whole corpus. Defaults to -1.
            num_threads (int, optional): Number of threads to execute the task on. Defaults to multiprocessing.cpu_count().

        Returns:
            dict: Keys are tuple of n-grams. Values are their counts.
        """
        print("Start generating n-grams...")
        self.execute_task(lambda text: self.count_n_grams(
            text, n), num_threads, batch_size, num_tweets)
        print()
        return self.counts

    def generate_collocation_counts(self, window_size, batch_size=1000, num_tweets=-1, num_threads=multiprocessing.cpu_count()):
        """Generate collocation counts from the corpus.

        Args:
            window_size (int): window size of collocations.
            batch_size (int, optional): Number of tweets to load at once from es. Defaults to 1000.
            num_tweets (int, optional): Number of tweets to use for the collocations count generation. When -1 uses whole corpus. Defaults to -1.
            num_threads (int, optional): Number of threads to execute the task on. Defaults to multiprocessing.cpu_count().

        Returns:
            dict: Keys are tuple of collocations. Values are their counts.
        """
        print("Start generating collocation counts...")
        self.execute_task(lambda text: self.count_collocations(
            text, window_size), num_threads, batch_size, num_tweets)
        print()
        return self.counts

    def generate_tokenized_tweets(self, batch_size=1000, num_tweets=-1, num_threads=multiprocessing.cpu_count()):
        """Generate a list of lists containing the tokenized tweets. Stop word and special character removal is applied.

        Args:
            batch_size (int, optional): Number of tweets to load at once from es. Defaults to 1000.
            num_tweets (int, optional): Number of tweets to use for the collocations count generation.
            When -1 uses whole corpus. Defaults to -1.
            num_threads (_type_, optional): Number of threads to execute the task on. Defaults to multiprocessing.cpu_count().

        Returns:
            _type_: list of lists containing tokenized tweets.
        """
        print("Start generating tokenized tweets...")
        self.execute_task(self.tokenize_tweet, num_threads, batch_size, num_tweets)
        print()
        return self.tokenized_tweets

    def generate_nes_collocation_counts(self, batch_size=1000, num_tweets=-1, num_threads=multiprocessing.cpu_count()):
        """Generate named entity collocation counts from the corpus.

        Args:
            batch_size (int, optional): Number of tweets to load at once from es. Defaults to 1000.
            num_tweets (int, optional): Number of tweets to use for the collocations count generation.
            When -1 uses whole corpus. Defaults to -1.
            num_threads (_type_, optional): Number of threads to execute the task on. Defaults to multiprocessing.cpu_count().

        Returns:
            _type_: dict containing collocations as tuple as keys and their respective counts as values.
        """
        print("Start counting named entity collocations...")
        self.execute_task(self.count_nes_collocations, num_threads, batch_size, num_tweets)
        print()
        return self.counts

    def generate_nes_counts(self, batch_size=1000, num_tweets=-1, num_threads=multiprocessing.cpu_count()):
        """Generate named entity counts from the corpus.

        Args:
            batch_size (int, optional): Number of tweets to load at once from es. Defaults to 1000.
            num_tweets (int, optional): Number of tweets to use for the collocations count generation.
            When -1 uses whole corpus. Defaults to -1.
            num_threads (_type_, optional): Number of threads to execute the task on.
            Defaults to multiprocessing.cpu_count().

        Returns:
            _type_: dict containing named entities and their types as tuple as keys and their respective counts as values.
        """
        print("Start counting named entities...")
        self.execute_task(self.count_nes, num_threads, batch_size, num_tweets)
        print()
        return self.counts
