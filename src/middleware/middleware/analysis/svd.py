from middleware.analysis.nlp_support import CorpusAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import scipy.linalg as linalg
from sklearn.decomposition import TruncatedSVD


class SVD:
    # Initialize variables and object instances
    def __init__(self):
        self.u_matrix = None
        self.s_matrix = None
        self.v_matrix = None
        self.corpus_analyzer = CorpusAnalyzer()
        self.corpus = None
        self.cv = None
        self.vocab = None
        self.vectors = None

    # Generates the SVD for a given number of tweets
    def generate_svd(self, num_tweets):
        # generate tokenized tweets and join them to form sentences
        self.corpus = self.corpus_analyzer.generate_tokenized_tweets(num_tweets=num_tweets)
        self.corpus = [' '.join(row) for row in self.corpus]

        self.cv = CountVectorizer()

        # generate document term matrix
        self.vectors = self.cv.fit_transform(self.corpus).todense()
        self.vocab = np.array(self.cv.get_feature_names_out())
        self.u_matrix, self.s_matrix, self.v_matrix = linalg.svd(self.vectors, full_matrices=False)
        return self.u_matrix, self.s_matrix, self.v_matrix

    # The truncated svd is not working properly since compnents_ is not found
    # Generates the Truncated SVD for a given number of tweets and number of topics
    # This SVD should be calculated much faster but is not as precise
    def generate_truncated_svd(self, num_topics, num_tweets=-1):
        if num_tweets == -1:
            f = open("./src/data/tokenized_tweets_nostop.linesentence", "r", encoding="utf_8")
            as_str = f.read()
            self.corpus = as_str.split("\n")
        else:
            self.corpus = self.corpus_analyzer.generate_tokenized_tweets(num_tweets=num_tweets)
            self.corpus = [' '.join(row) for row in self.corpus]
        print("Loaded corpus")

        self.cv = CountVectorizer()
        self.vectors = self.cv.fit_transform(self.corpus)
        print("Calculated word counts")
        self.vocab = np.array(self.cv.get_feature_names_out())
        svd = TruncatedSVD(n_components=num_topics, random_state=42)

        self.u_matrix = svd.fit_transform(self.vectors)
        print("Calculated SVD")
        self.s_matrix = np.diag(svd.singular_values_)
        self.v_matrix = svd.components_
        return self.u_matrix, self.s_matrix, self.v_matrix

    # Display the top words for each
    def show_topics(self, num_top_words=8, num_topics=10):
        top_words = lambda t: [self.vocab[i] for i in np.argsort(t)[:-num_top_words - 1:-1]]
        topic_words = ([top_words(t) for t in self.v_matrix[:num_topics, :]])
        return [' '.join(t) for t in topic_words]

    def print_topics(self, num_top_words=8, num_topics=10):
        reconstructed_vectors = self.u_matrix @ np.diag(self.s_matrix) @ self.v_matrix
        print(np.linalg.norm(reconstructed_vectors - self.vectors))
        print(np.allclose(reconstructed_vectors, self.vectors))
        print(np.allclose(self.u_matrix.T @ self.u_matrix, np.eye(self.u_matrix.shape[0])))
        print(np.allclose(self.v_matrix @ self.v_matrix.T, np.eye(self.v_matrix.shape[0])))
        print(self.show_topics(num_top_words, num_topics))
