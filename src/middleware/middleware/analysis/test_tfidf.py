from middleware.analysis.nlp_support import CorpusAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Test_TF_IDF:
    def __init__(self):
        self.corpus_analyzer = CorpusAnalyzer()
        self.corpus = None
        self.tf_idf_matrix = None
        self.similarity_matrix = None
        self.vocabulary = None

    def calculate_tf_idf(self, num_tweets=1, min_df=3,max_df=0.85):
        self.corpus = self.corpus_analyzer.generate_tokenized_tweets(num_tweets=num_tweets)
        self.corpus = [' '.join(row) for row in self.corpus]

        # Count term appearances
        count_vectorizer = CountVectorizer()
        count_matrix = count_vectorizer.fit_transform(self.corpus)
        self.vocabulary = count_vectorizer.vocabulary_

        # Calculate tf-idf values
        tf_idf_transformer = TfidfTransformer()
        self.tf_idf_matrix = tf_idf_transformer.fit_transform(count_matrix).toarray()
        return self.tf_idf_matrix
    
    def calculate_cosine_similarity(self,num_tweets = 1, min_df=5,max_df=0.85):
        if self.tf_idf_matrix == None:
            self.tf_idf_matrix = self.calculate_tf_idf(num_tweets,min_df,max_df)
        self.similarity_matrix = cosine_similarity(self.tf_idf_matrix)
        return self.similarity_matrix

    def n_highest_mean_tfidf(self,n=10):
        A = np.array(self.tf_idf_matrix)
        # calculate the average value of each column
        column_averages = np.mean(A, axis=0)

        # find the indices of the 5 largest elements in the column_averages array
        indices = np.argpartition(column_averages, -n)[-n:]

        # get the 5 columns of A with the highest average value
        most_average_columns = A[:, indices]
        # calculate the mean of the most average columns
        mean_of_most_average_columns = np.mean(most_average_columns,axis=0)

        most_average_words = [word for word, index in self.vocabulary.items() if index in indices]
        result = [[most_average_words[i], mean_of_most_average_columns[i]] for i in range(n)]
        return result
    
    def n_highest_sum_tfidf(self,n=10):
        A = np.array(self.tf_idf_matrix)
        # calculate the sum value of each column
        column_averages = np.sum(A, axis=0)

        # find the indices of the 5 largest elements in the column_sum array
        indices = np.argpartition(column_averages, -n)[-n:]

        # get the 5 columns of A with the highest sum value
        most_sum_columns = A[:, indices]
        # calculate the mean of the most sum columns
        total_of_most_sum_columns = np.sum(most_sum_columns,axis=0)

        most_sum_words = [word for word, index in self.vocabulary.items() if index in indices]
        result = [[most_sum_words[i], total_of_most_sum_columns[i]] for i in range(n)]
        return result

    def most_similar_tweets(self,n=20):
        k = []
        sorted_k = []

        for i in range(len(self.similarity_matrix)):
            for j in range(i+1,len(self.similarity_matrix[0])):
                if i != j:
                    if self.corpus[i] != self.corpus[j]:
                        k.append([self.corpus[i], self.corpus[j], self.similarity_matrix[i][j]])

        # sort k based on the third element (self.similarity_matrix[i][j]) in descending order
        sorted_k = sorted(k, key=lambda x: x[2], reverse=True)

        # keep only the n highest values of matrix[i][j]
        sorted_k = sorted_k[:n]

        return sorted_k

    def least_similar_tweets(self,n=20):
        k = []
        sorted_k = []

        for i in range(len(self.similarity_matrix)):
            for j in range(i+1,len(self.similarity_matrix[0])):
                if i != j:
                    if self.corpus[i] != self.corpus[j]:
                        k.append([self.corpus[i], self.corpus[j], self.similarity_matrix[i][j]])

        # sort k based on the third element (self.similarity_matrix[i][j]) in ascending order
        sorted_k = sorted(k, key=lambda x: x[2])

        # keep only the n lowest values of matrix[i][j]
        sorted_k = sorted_k[:n]

        return sorted_k
