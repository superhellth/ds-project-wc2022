from middleware.analysis import test_tfidf
import numpy as np
from middleware.analysis import nmf

topic = nmf.NMF_topic_modeling()
topic.calculate_nmf(1000)
topic.print_results(10,5)