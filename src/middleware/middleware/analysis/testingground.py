from middleware.analysis import test_tfidf
import numpy as np
tfidf = test_tfidf.Test_TF_IDF()
matrix = tfidf.calculate_cosine_similarity(num_tweets=1000)

"""k=tfidf.most_similar_tweets()
for i in range(len(k)):
    print("____________________")
    print(k[i])
    print("____________________")
print(len(k))
print(tfidf.vocabulary)"""
x= tfidf.n_highest_sum_tfidf()
print(x)