from middleware.analysis.nlp_support import CorpusAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import scipy.linalg as linalg
from sklearn.decomposition import TruncatedSVD

class SVD:
    # Initialize variables and object instances
    def __init__(self):
        self.document_term_matrix = None
        self.u_matrix = None
        self.s_matrix = None
        self.v_matrix = None
        self.corpus_analyzer = CorpusAnalyzer()
        self.corpus = None
        self.cv = None
        self.vocab = None
        self.vectors = None
    
    # Generates the SVD for a given number of tweets
    def generate_svd(self,num_tweets):
        # generate tokenized tweets and join them to form sentences
        self.corpus = self.corpus_analyzer.generate_tokenized_tweets(num_tweets=num_tweets)
        self.corpus = [' '.join(row) for row in self.corpus]

        self.cv = CountVectorizer()

        # generate document term matrix
        self.vectors = self.cv.fit_transform(self.corpus).todense()
        self.vocab = np.array(self.cv.get_feature_names_out())
        self.u_matrix, self.s_matrix, self.v_matrix = linalg.svd(self.vectors, full_matrices=False)
        return self.u_matrix, self.s_matrix, self.v_matrix

    #The truncated svd is not working properly since compnents_ is not found
     # Generates the Truncated SVD for a given number of tweets and number of topics
     # This SVD should be calculated much faster but is not as precise
    """def generate_truncated_svd(self,num_tweets,num_topics=10):
        self.corpus = self.corpus_analyzer.generate_tokenized_tweets(num_tweets=num_tweets)
        self.corpus = [' '.join(row) for row in self.corpus]

        self.cv = CountVectorizer()
        self.vectors = self.cv.fit_transform(self.corpus).todense()
        self.vocab = np.array(self.cv.get_feature_names_out())
        truncated_svd = TruncatedSVD(n_components=100)
        self.vectors = np.asarray(self.cv.fit_transform(self.corpus).todense())
        self.u_matrix = truncated_svd.components_
        self.s_matrix = truncated_svd.singular_values_
        self.v_matrix = np.dot(self.u_matrix, np.diag(self.s_matrix))
        return self.u_matrix, self.s_matrix, self.v_matrix"""
    

    # Display the top words for each
    def show_topics(self,num_top_words=8,num_topics=10):
        top_words = lambda t: [self.vocab[i] for i in np.argsort(t)[:-num_top_words-1:-1]]
        topic_words = ([top_words(t) for t in self.v_matrix[:num_topics]])
        return [' '.join(t) for t in topic_words]
    
    def print_topics(self,num_top_words=8,num_topics=10):
        u,s,v = self.generate_truncated_svd(num_tweets=1000,num_topics=10)
        reconstructed_vectors = u @ np.diag(s) @ v
        print(np.linalg.norm(reconstructed_vectors - self.vectors))
        print(np.allclose(reconstructed_vectors, self.vectors))
        print(np.allclose(u.T @ u, np.eye(u.shape[0])))
        print(np.allclose(v @ v.T, np.eye(v.shape[0])))
        print(self.show_topics(num_top_words,num_topics))

