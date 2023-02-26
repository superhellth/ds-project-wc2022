from middleware.analysis import test_tfidf
from middleware.analysis import svd
from middleware.analysis import nmf

"""tm = svd.SVD()

NUM_TOPICS = 30

tm.generate_truncated_svd(num_topics=NUM_TOPICS, num_tweets=-1)
print(tm.show_topics(num_top_words=8, num_topics=NUM_TOPICS))"""

NUM_TWEETS = 1000 #Number of tweets which are considered
NUM_TOPICS = 8 #Number of the most prominent topics which are geting extracted
NUM_TOP_WORDS = 8 #Number of words a topic is described by
test_nmf = nmf.NMF_topic_modeling()
test_nmf.calculate_nmf(NUM_TWEETS)
print(test_nmf.show_topics(test_nmf.topic_term_matrix[:NUM_TOPICS, :],NUM_TOP_WORDS,list(test_nmf.cv.vocabulary_.keys())))
