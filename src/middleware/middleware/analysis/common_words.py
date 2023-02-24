# File is just for getting used to the framework
from middleware.analysis import tweet_provider
from middleware.analysis.nlp_support import CorpusAnalyzer
from collections import Counter
from itertools import chain


class CommonWords:
    def __init__(self):
        self.provider = tweet_provider.TweetProvider()
        self.corpus_analyzer = CorpusAnalyzer()

    def calculate_common_words(self, corpus_size=1000, common=50):
        Corpus = self.provider.get_corpus(corpus_size)
        tokenized_corpus = []

        for str in Corpus:
            tokenized_corpus.append(self.corpus_analyzer.tokenize(str, use_advanced_tokenize=True, lemmatize=True))

        word_counter = Counter(chain.from_iterable(tokenized_corpus))

        return word_counter.most_common(common)
