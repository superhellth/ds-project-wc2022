from middleware.analysis.sentiment_vaderSentiment import VaderSentiment
from middleware.analysis.sentiment_BERT import BERTSentiment
from middleware.analysis.sentiment_logregclass import LogRegClass


DID_INIT_SENTIMENT_ANALYZERS = False
VSENT = None
LRCOther = None
LRCOwn = None
BERTSENT = None


def get_sentiment_analyzers(path_to_sentiment_models, path_to_other_training_data, path_to_other_test_data,
                            path_to_own_training_data, path_to_own_test_data):
    global VSENT, LRCOther, LRCOwn, BERTSENT, DID_INIT_SENTIMENT_ANALYZERS
    if VSENT is None or LRCOther is None or LRCOwn is None or BERTSENT:
        VSENT = VaderSentiment("vaderSent")
        LRCOther = LogRegClass("logRegClassOther", path_to_sentiment_models, path_to_other_training_data,
                                            path_to_other_test_data)
        LRCOwn = LogRegClass("logRegClassOwn", path_to_sentiment_models, path_to_own_training_data,
                             path_to_own_test_data)
        BERTSENT = BERTSentiment("bertClassSent")
    return VSENT, LRCOther, LRCOwn, BERTSENT
