from middleware.analysis import test_tfidf
from middleware.analysis import svd

tm = svd.SVD()

NUM_TOPICS = 15

tm.generate_truncated_svd(num_topics=NUM_TOPICS, num_tweets=-1)
print(tm.show_topics(num_top_words=15,num_topics=NUM_TOPICS))
