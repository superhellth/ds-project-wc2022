import re
from abc import ABC
from typing import List, Tuple, Dict

from middleware.analysis.sentiment_base import SentimentBase
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


class BERTSentiment(SentimentBase, ABC):
    def __init__(self, model_name):
        super().__init__(model_name)
        self.pipe = None
        self.tokenizer = None
        self.model = None
        if not self.did_train:
            self.train_and_save_model()

    def preprocess_text(self, text: str) -> str:
        new_text = []
        for t in text.split(" "):
            t = t if re.match(r'[A-Za-z0-9\'\s]', t) else ""
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    @staticmethod
    def __map_sent_to_number(sentiment_dict: dict) -> float:
        score = sentiment_dict[0]['score']
        if sentiment_dict[0]['label'] == 'negative':
            return score * -1
        elif sentiment_dict[0]['label'] == 'positive':
            return score
        else:
            return 0

    def get_sentiment_of_text(self, text: str) -> float:
        return self.__map_sent_to_number(self.pipe(self.preprocess_text(text)))

    def get_sentiment_of_text_list(self, texts: List[str]) -> List[float]:
        res = []
        for text in texts:
            res.append(self.__map_sent_to_number(self.pipe(self.preprocess_text(text))))
        return res

    def get_average_sentiment_of_text_list(self, texts: List[str]) -> float:
        res = []
        for text in texts:
            res.append(self.__map_sent_to_number(self.pipe(self.preprocess_text(text))))
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
        self.tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.pipe = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer, max_length=512,
                             truncation=True)
        self.did_train = True
