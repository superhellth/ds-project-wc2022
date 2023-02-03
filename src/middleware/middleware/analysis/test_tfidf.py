from middleware.analysis.nlp_support import CorpusAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np

class Test_TF_IDF:
    def __init__(self):
        self.corpus_analyzer = CorpusAnalyzer()
        self.corpus = None

    def calculate_tf_idf(self, num_tweets=1, min_df=3,max_df=0.85):
        self.corpus = self.corpus_analyzer.generate_tokenized_tweets(num_tweets=num_tweets)
        #self.corpus = [item for sublist in self.corpus for item in sublist]
        self.corpus = [' '.join(row) for row in self.corpus]

        # Count term appearances
        count_vectorizer = CountVectorizer()
        count_matrix = count_vectorizer.fit_transform(self.corpus)
        id_term_dict = {id: term for (term, id) in count_vectorizer.vocabulary_.items()}
        num_terms = count_matrix.shape[1]
        #print(f"Total number of terms: {num_terms}")

        # Calculate tf-idf values
        tf_idf_transformer = TfidfTransformer()
        tf_idf_matrix = tf_idf_transformer.fit_transform(count_matrix).toarray()
        return tf_idf_matrix
    
    def calculate_cosine_similarity(self,num_tweets = 1, min_df=5):
        matrix = self.calculate_tf_idf(num_tweets,min_df)
        similarity_matrix = cosine_similarity(matrix)
        return similarity_matrix
       
    def get_cosine(self,i,j,matrix):
        return cosine_similarity(matrix[i],matrix[j])
