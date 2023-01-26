from abc import ABC
from typing import List, Tuple, Dict

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from middleware.analysis.sentiment_base import SentimentBase


class BERTSentiment(SentimentBase, ABC):
    def __init__(self, model_name):
        super().__init__(model_name)
        self.model = SentimentIntensityAnalyzer()
