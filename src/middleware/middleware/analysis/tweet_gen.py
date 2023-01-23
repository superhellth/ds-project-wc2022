import string
from middleware.analysis import stat_provider

class TweetGenerator:

    def __init__(self, provider: stat_provider.StatProvider) -> None:
        self.stat_provider = provider
        self.used_n_grams = []

    def get_next_n_gram(self, current_string: str, n: int, percent_n_grams: float, allow_repition: bool):
        """Return next moste likely n-gram."""
        current_words = current_string.split()
        if n > 1:
            current_last_words = " ".join(current_words[-(n-1):])
        else:
            current_last_words = ""
        next_n_gram = self.stat_provider.get_n_gram_that(n=n, starts_with=current_last_words, not_in=self.used_n_grams, top_percent=percent_n_grams)
        if not allow_repition:
            self.used_n_grams.append(next_n_gram)
        return next_n_gram

    def gen_tweet_from(self, given: str, length, n, percent_n_grams, allow_repition):
        self.used_n_grams = []
        given = given.lower().strip().translate(str.maketrans("", "", string.punctuation))
        for i in range(length):
            next_n_gram = self.get_next_n_gram(given, n, percent_n_grams, allow_repition)
            if next_n_gram == ():
                break
            given += " " + next_n_gram[n - 1]
        return given.strip()
