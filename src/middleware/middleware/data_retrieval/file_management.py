from middleware.analysis.sentiment_vaderSentiment import VaderSentiment
from middleware.analysis.sentiment_trained_classifier import TrainedClassifierSentiment
from middleware.analysis.sentiment_NB import NBSentiment
from middleware.analysis.sentiment_BERT import BERTSentiment


DID_INIT_SENTIMENT_ANALYZERS = False
VSENT = None
TCSENT = None
NBSENT = None
BERTSENT = None


def get_sentiment_analyzers():
    global VSENT, TCSENT, NBSENT, BERTSENT, DID_INIT_SENTIMENT_ANALYZERS
    if VSENT is None or TCSENT is None or NBSENT is None or BERTSENT:
        VSENT = VaderSentiment("vaderSent")
        TCSENT = TrainedClassifierSentiment("trainedClassSent")
        NBSENT = NBSentiment("nbClassSent")
        BERTSENT = BERTSentiment("bertClassSent")
    return VSENT, TCSENT, NBSENT, BERTSENT
