from middleware.analysis import test_tfidf
from middleware.analysis import svd

tm = svd.SVD()

tm.generate_truncated_svd(100000,num_topics=10)
print(tm.show_topics(num_top_words=8,num_topics=10))
