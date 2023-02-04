from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from middleware.analysis.nlp_support import CorpusAnalyzer
import numpy as np

class NMF_topic_modeling:
    def __init__(self):
        self.corpus_analyzer = CorpusAnalyzer()
        self.corpus = None
        self.document_topic_matrix = None
        self.topic_term_matrix = None
        self.cv = None
        self.model = None
    
    def calculate_nmf(self,num_tweets):
        self.corpus = self.corpus_analyzer.generate_tokenized_tweets(num_tweets=num_tweets)
        self.corpus = [' '.join(row) for row in self.corpus]

        self.cv = CountVectorizer(input="content", max_features=10000)
        matrix = self.cv.fit_transform(self.corpus)

        self.model = NMF(n_components=10, random_state=42,max_iter=500)
        self.document_topic_matrix = self.model.fit_transform(matrix)
        self.topic_term_matrix = self.model.components_

    def show_topics(self,components,num_top_words,vocab):
        #for each component or topic sorts the row values from large to small and 
        # returns the top words as the representation of the topic.
        top_words = lambda t: [vocab[i] for i in np.argsort(t)[:-num_top_words-1:-1]]
        topic_words = ([top_words(t) for t in components])
        return [' '.join(t) for t in topic_words]
    
    def print_results(self,num_topics,num_top_words):
        print(self.topic_term_matrix.shape)
        print(self.topic_term_matrix[:2,:].shape)
        print(self.show_topics(self.topic_term_matrix[:num_topics,:], num_top_words, list(self.cv.vocabulary_.keys())))
