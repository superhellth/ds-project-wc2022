import os.path
from abc import ABC
from typing import List, Tuple, Dict

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

from middleware.analysis.sentiment_base import SentimentBase


class NBSentiment(SentimentBase, ABC):
    def __init__(self, model_name, path_to_models, path_to_training_data, path_to_test_data):
        super().__init__(model_name, path_to_model=path_to_models + model_name,
                         path_to_training_data=path_to_training_data,
                         path_to_test_data=path_to_test_data)
        if not os.path.exists(self.path_to_model + "classifier" + ".joblib" or self.path_to_model + "vectorizer" +
                              ".joblib"):
            self.train_and_save_model()
        self.classifier = joblib.load(self.path_to_model + "classifier" + ".joblib")
        self.vectorizer = joblib.load(self.path_to_model + "vectorizer" + ".joblib")


    def preprocess_text(self, text):
        pass

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
        tweets = pd.read_csv(self.path_to_training_data)
        tweets.dropna(inplace=True)
        tweets_text = tweets["selected_text"]
        tweets_sentiment = tweets["sentiment"]

        # convert the labels to integers ("positive" -> 3, "neutral" -> 2, "negative" -> 1)
        labels = [3 if label == "positive" else 2 if label == "neutral" else 1 for label in tweets_sentiment]

        # use a TfidfVectorizer to convert the text to numerical features
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(tweets_text)

        # train a SGDClassifier model on the training data
        classifier = MultinomialNB()
        classifier.fit(X, labels)

        joblib.dump(classifier, self.path_to_model + "classifier" + ".joblib")
        joblib.dump(vectorizer, self.path_to_model + "vectorizer" + ".joblib")
        self.did_train = True

    def accuracy(self):
        # load your labeled tweet dataset
        tweets = pd.read_csv(self.path_to_test_data)
        tweets.dropna(inplace=True)
        tweets_text = tweets["selected_text"]
        tweets_sentiment = tweets["sentiment"]
        labels = [3 if label == "positive" else 2 if label == "neutral" else 1 for label in tweets_sentiment]
        tweets_text_vec = self.vectorizer(tweets_text)
        predictions = self.classifier.predict(tweets_text_vec)
        return sum([1 if predictions[i] == labels[i] else 0 for i in range(len(labels))])
