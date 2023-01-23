import json
import ast
import spacy

class StatProvider:
    """Provides python dicts etc. containing n-grams, collocations counts..."""

    def __init__(self, path_to_data_files):      
        self.nlp = spacy.load("en_core_web_sm")
        self.n_gram_files = ["unigrams.json", "bigrams.json", "trigrams.json"]
        self.collocation_files = ["collocations2.json", "collocations3.json", "collocations4.json"]
        self.path_to_data_files = path_to_data_files
        self.n_grams = [{}, {}, {}]
        self.sorted_n_grams = [[], [], []]
        self.collocations_counts = [{}, {}, {}]
        self.sorted_collocation_counts = [[], [], []]

    def load_n_grams(self, n):
        """Loads *grams.json into dict."""
        f = open(self.path_to_data_files + self.n_gram_files[n-1], "r", encoding="utf_8")
        n_gram_dict = json.loads(f.read())
        self.n_grams[n-1] = n_gram_dict

    def load_collocation_counts(self, window_size):
        """Loads collocations*.json into dict."""
        f = open(self.path_to_data_files + self.collocation_files[window_size - 2], "r", encoding="utf_8")
        collocation_dict = json.loads(f.read())
        self.collocations_counts[window_size - 2] = collocation_dict

    def get_n_grams_as_dict(self, n):
        """Return complete dict of n-gram counts."""
        if not self.n_grams[n-1]:
            self.load_n_grams(n)
        return self.n_grams[n-1]

    def get_collocations_as_dict(self, window_size):
        """Return complete dict of collocation counts."""
        if not self.collocations_counts[window_size - 2]:
            self.load_collocation_counts(window_size)
        return self.collocations_counts[window_size - 2]

    def get_n_grams_as_list(self, n):
        """Return complete sorted list of n-grams including their counts."""
        if not self.sorted_n_grams[n-1]:
            self.sorted_n_grams[n-1] = sorted(self.get_n_grams_as_dict(n).items(), key=lambda x: x[1], reverse=True)
        return self.sorted_n_grams[n-1]

    def get_collocations_as_list(self, window_size):
        """Return complete sorted list of collocations including their counts."""
        if not self.sorted_collocation_counts[window_size - 2]:
            self.sorted_collocation_counts[window_size - 2] = sorted(self.get_collocations_as_dict(window_size).items(), key=lambda x: x[1], reverse=True)
        return self.sorted_collocation_counts[window_size - 2]

    def get_n_gram_that(self, n, starts_with, not_in=[], top_percent=0.2):
        """Get the most probable n-gram that matches the criteria.

        Args:
            n (int): n-gram size.
            starts_with (string): The resulting n-gram has to start with this string.
            not_in (list, optional): List of n-grams. Functions as a blacklist for the resulting n-gram. Defaults to [].
            top_percent (float, optional): For performance reasons. Only consider the top_percent percent of n-grams. Defaults to 0.2.

        Returns:
            tuple: n-gram as tuple. () is no n-gram matches the criteria.
        """
        sorted_n_gram_list = self.get_n_grams_as_list(n)
        for i, entry in enumerate(sorted_n_gram_list[:round(len(sorted_n_gram_list) * top_percent)]):
            n_gram = entry[0]
            if n > 1:
                n_gram = " ".join(ast.literal_eval(n_gram))
            if n_gram.startswith(starts_with):
                candidate = tuple(n_gram.split())
            else:
                continue
            if candidate not in not_in:
                return candidate
        return ()

    def get_top_unigrams(self, k=10, include_stop_words=False, only_hashtags=False, only_mentions=False):
        """Return top k unigrams."""
        sorted_unigrams = self.get_n_grams_as_list(1)

        result = []
        i = 0
        j = 0
        while i < k:
            token = sorted_unigrams[j][0]
            if include_stop_words or token not in self.nlp.Defaults.stop_words:
                if not only_hashtags or (only_hashtags and token[0] == "#"):
                    if not only_mentions or (only_mentions and token[0] == "@"):
                        result.append(sorted_unigrams[j])
                        i += 1
            j += 1

        return {entry[0]: entry[1] for entry in result}

    def get_top_n_grams(self, n, k=10):
        """Return top k n-grams."""
        return {entry[0]: entry[1] for entry in self.get_n_grams_as_list(n)[:k]}
