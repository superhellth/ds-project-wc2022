from abc import ABC
from typing import List, Tuple, Dict

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from middleware.analysis.sentiment_base import SentimentBase


class BERTSentiment(SentimentBase, ABC):
    def __init__(self, model_name):
        super().__init__(model_name)
        self.model = SentimentIntensityAnalyzer()

    def get_sentiment_of_text(self, text) -> float:
        return self.model.polarity_scores(text)['compound']

    def get_sentiment_of_text_list(self, texts) -> List[float]:
        res = []
        for text in texts:
            res.append(self.model.polarity_scores(text)['compound'])
        return res

    def get_average_sentiment_of_text_list(self, texts) -> float:
        res = []
        for text in texts:
            res.append(self.model.polarity_scores(text)['compound'])
        return sum(res) / len(texts)

    def get_sentiment_of_text_list_by_date(self, texts: List[Tuple[str, str]]) -> Dict:
        """
        Returns average sent by every day/week/month. Be careful to generate the date such that the output can be
        grouped by date.
        """
        partitioned_lists = {}

        for text, date in texts:
            if date not in partitioned_lists:
                partitioned_lists[date] = []
            partitioned_lists[date].append(text)

        for k, v in partitioned_lists.items():
            partitioned_lists[k] = self.get_average_sentiment_of_text_list(v)

        return partitioned_lists

    def train_and_save_model(self):
        """
        No training required.
        """
        self.did_train = True

