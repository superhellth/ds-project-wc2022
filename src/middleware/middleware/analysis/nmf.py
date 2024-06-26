from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from middleware.analysis.nlp_support import CorpusAnalyzer
import numpy as np


class NMF_topic_modeling:
    # initialize the class with corpus_analyzer object, corpus and document_topic_matrix and topic_term_matrix variables
    def __init__(self):
        self.corpus_analyzer = CorpusAnalyzer()
        self.corpus = None
        self.document_topic_matrix = None
        self.topic_term_matrix = None
        self.cv = None
        self.model = None

    def calculate_nmf(self, num_tweets):
        if num_tweets == -1:
            f = open("./src/data/tokenized_tweets_nostop.linesentence",
                     "r", encoding="utf_8")
            as_str = f.read()
            self.corpus = as_str.split("\n")[0:1000000]
        else:
            # generate tokenized tweets and join them to form sentences
            self.corpus = self.corpus_analyzer.generate_tokenized_tweets(
                num_tweets=num_tweets)
            self.corpus = [' '.join(row) for row in self.corpus]
        print("Loaded corpus")

        # instantiate the count vectorizer object with max_features = 10000
        self.cv = CountVectorizer(input="content", max_features=10000)
        # fit the count vectorizer on corpus
        matrix = self.cv.fit_transform(self.corpus)
        print("Calculated word counts")

        self.model = NMF(n_components=50, random_state=42, max_iter=500)
        self.document_topic_matrix = self.model.fit_transform(matrix)
        print("Calculated NMF")

        # get the topic-term matrix from the model
        self.topic_term_matrix = self.model.components_

    # method to return the top words for each topic
    def show_topics(self, components, num_top_words, vocab):
        # for each component or topic sorts the row values from large to small and
        # returns the top words as the representation of the topic.
        def top_words(t): return [vocab[i]
                                  for i in np.argsort(t)[:-num_top_words - 1:-1]]
        topic_words = ([top_words(t) for t in components])
        return [' '.join(t) for t in topic_words]

    # method to print the results, i.e., the shape of the topic-term matrix and the top words for each topic
    # num_topics = number of topics, num_top_words = Number of the most prominent topics which are geting extracted
    # list(self.cv.vocabulary_.keys()) = vocabulary build on the loaded tweets transformed to a list
    def print_results(self, num_topics, num_top_words):
        print(self.topic_term_matrix.shape)
        print(self.topic_term_matrix[:2, :].shape)
        print(self.show_topics(self.topic_term_matrix[:num_topics, :], num_top_words, list(
            self.cv.vocabulary_.keys())))
