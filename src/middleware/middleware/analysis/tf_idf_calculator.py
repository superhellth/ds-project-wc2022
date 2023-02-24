from middleware.analysis.nlp_support import CorpusAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np


class TfIdfCalculator:
    def __init__(self):
        self.corpus_analyzer = CorpusAnalyzer()
        self.corpus = None

    def calculate_tf_idf(self, num_tweets=1, min_df=3, max_df=0.85):
        self.corpus = self.corpus_analyzer.generate_tokenized_tweets(num_tweets=num_tweets)
        self.corpus = [" ".join(tweet) for tweet in self.corpus]

        # Count term appearances
        stop = list(spacy.lang.en.stop_words.STOP_WORDS) + ['ll', 've']
        count_vectorizer = CountVectorizer(stop_words=stop, min_df=min_df, max_df=0.85)
        count_matrix = count_vectorizer.fit_transform(self.corpus)
        id_term_dict = {id: term for (term, id) in count_vectorizer.vocabulary_.items()}
        num_terms = count_matrix.shape[1]
        print(f"Total number of terms: {num_terms}")

        # Calculate tf-idf values
        tf_idf_transformer = TfidfTransformer(sublinear_tf=True,
                                              norm="l2")  # Modifed parameter because values have been higher than one
        tf_idf_matrix = tf_idf_transformer.fit_transform(count_matrix).toarray()
        return tf_idf_matrix

    def calculate_cosine_similarity(self, num_tweets=1, min_df=5):
        matrix = self.calculate_tf_idf(num_tweets, min_df)
        similarity_matrix = cosine_similarity(matrix)
        return similarity_matrix

    def get_top_n_indices(self, matrix, n):
        upper_triangle_indices = np.triu_indices(matrix.shape[0], k=1)
        # Get the values of the upper triangle
        upper_triangle_values = matrix[upper_triangle_indices]
        # Get the indices of the top n values
        flat_indices = np.argpartition(-upper_triangle_values, n)[n:]
        top_n_values = upper_triangle_values[flat_indices]
        # Store the original indices
        multi_indices = [np.unravel_index(flat_index, matrix.shape) for flat_index in flat_indices]
        return top_n_values, multi_indices

    def nth_simiular_tweets(self, num_tweets=1, min_df=5, n=5):
        similarity_matrix = self.calculate_cosine_similarity(num_tweets, min_df=1)
        top_n_values, multi_indices = self.get_top_n_indices(similarity_matrix, n)
        top_score_tweets = []
        for i in range(n):
            top_score_tweets.append(
                [top_n_values[i], self.corpus[multi_indices[i][0]], self.corpus[multi_indices[i][1]]])

        return top_score_tweets
