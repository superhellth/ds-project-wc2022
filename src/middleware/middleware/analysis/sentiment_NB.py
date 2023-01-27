from abc import ABC
from typing import List, Tuple, Dict

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

from middleware.analysis.sentiment_base import SentimentBase


class NBSentiment(SentimentBase, ABC):
    def __init__(self, model_name):
        super().__init__(model_name)
        self.vectorizer = None
        self.classifier = None
        self.data_file_path = '/Users/bastianmuller/Desktop/Programming/Python/testing/ds-project-wc2022/src/data/Tweets.csv'
        self.model_path = '/Users/bastianmuller/Desktop/Programming/Python/testing/ds-project-wc2022/src/middleware/middleware/analysis/sentiment_models/' + self.model_name + '.joblib'
        if not self.did_train:
            self.train_and_save_model()
        self.model = joblib.load(self.model_path)

    def get_sentiment_of_text(self, text) -> float:
        vec_tweet = self.vectorizer.transform([text])
        return int(self.classifier.predict(vec_tweet)) - 2

    def get_sentiment_of_text_list(self, texts) -> List[float]:
        res = []
        for text in texts:
            vec_tweet = self.vectorizer.transform([text])
            res.append(self.classifier.predict(vec_tweet))
        return [int(e) - 2 for e in res]

    def get_average_sentiment_of_text_list(self, texts) -> float:
        res = []
        for text in texts:
            vec_tweet = self.vectorizer.transform([text])
            res.append(int(self.classifier.predict(vec_tweet)))
        return sum(res) / len(texts) - 2.0

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
        # load your labeled tweet dataset
        tweets = pd.read_csv(self.data_file_path)
        tweets.dropna(inplace=True)
        tweets_text = tweets["selected_text"]
        tweets_sentiment = tweets["sentiment"]

        # convert the labels to integers ("positive" -> 3, "neutral" -> 2, "negative" -> 1)
        labels = [3 if label == "positive" else 2 if label == "neutral" else 1 for label in tweets_sentiment]

        # use a TfidfVectorizer to convert the text to numerical features
        self.vectorizer = CountVectorizer()
        X = self.vectorizer.fit_transform(tweets_text)

        # split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2)

        # train a SGDClassifier model on the training data
        self.classifier = MultinomialNB()
        self.classifier.fit(X_train, y_train)

        joblib.dump(self.classifier, self.model_path)
        self.did_train = True
