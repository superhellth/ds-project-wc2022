from middleware.analysis import test_tfidf
from middleware.analysis import svd

tm = svd.SVD()

tm.generate_svd(num_tweets=10000)
print(tm.show_topics())
