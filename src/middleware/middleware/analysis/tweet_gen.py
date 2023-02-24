import string
from middleware.analysis import stat_provider


class TweetGenerator:
    """This class predicts how tweets may be continued, based on n-gram staticstics.
    """

    def __init__(self, provider: stat_provider.StatProvider) -> None:
        self.stat_provider = provider
        self.used_n_grams = []

    def get_next_n_gram(self, current_string: str, n: int, percent_n_grams: float, allow_repition: bool):
        """Return the n-gram that is the most likely to follow the given string, matching the criteria.

        Args:
            current_string (str): String to complete.
            n (int): Size of n-grams to make the prediction.
            percent_n_grams (float): Percentage of n-grams to consider. Only for performance reasons. High percentage leads to better result but worse performance.
            allow_repition (bool): Allow repition of n-grams.

        Returns:
            tuple: Predicted n-gram as tuple.
        """
        current_words = current_string.split()
        if n > 1:
            current_last_words = " ".join(current_words[-(n - 1):])
        else:
            current_last_words = ""
        next_n_gram = self.stat_provider.get_n_gram_that(
            n=n, starts_with=current_last_words, not_in=self.used_n_grams, top_percent=percent_n_grams)
        if not allow_repition:
            self.used_n_grams.append(next_n_gram)
        return next_n_gram

    def gen_tweet_from(self, given: str, length, n, percent_n_grams, allow_repition):
        """Complete a tweet using the given rules.

        Args:
            given (str): The (tweet) string to complete.
            length (int): Number of tokens to generate following the given text.
            n (int): Size of n-grams to use.
            percent_n_grams (float): Percentage of n-grams to consider for the prediction. Only for performance reasons.
            allow_repition (bool): Allow repition of n-grams in the predicted part of the text.

        Returns:
            string: Completed tweet text.
        """
        self.used_n_grams = []
        given = given.lower().strip().translate(
            str.maketrans("", "", string.punctuation))
        for i in range(length):
            next_n_gram = self.get_next_n_gram(
                given, n, percent_n_grams, allow_repition)
            if next_n_gram == ():
                break
            given += " " + next_n_gram[n - 1]
        return given.strip()
