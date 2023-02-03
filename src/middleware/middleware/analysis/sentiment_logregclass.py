import os.path
import re
from abc import ABC
from typing import List, Tuple, Dict

import joblib
import pandas as pd
import spacy
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer

from middleware.analysis.sentiment_base import SentimentBase


class LogRegClass(SentimentBase, ABC):
    def __init__(self, model_name, path_to_models, path_to_training_data, path_to_test_data):
        super().__init__(model_name, path_to_model=path_to_models + model_name,
                         path_to_training_data=path_to_training_data,
                         path_to_test_data=path_to_test_data)
        self.en = spacy.load('en_core_web_sm')
        self.stopwords = self.en.Defaults.stop_words
        if not os.path.exists(self.path_to_model + "classifier" + ".joblib" or self.path_to_model + "vectorizer" +
                              ".joblib"):
            self.train_and_save_model()

        self.classifier = joblib.load(self.path_to_model + "classifier" + ".joblib")
        self.vectorizer = joblib.load(self.path_to_model + "vectorizer" + ".joblib")

    def preprocess_text(self, text: str):
        text = text.lower()
        new_text = []
        for t in text.split(" "):
            t = t if re.match(r'[a-z\'\s@]', t) else ""
            t = t if t not in self.stopwords else ""
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def get_sentiment_of_text(self, text) -> float:
        vec_tweet = self.vectorizer.transform([self.preprocess_text(text)])
        return int(self.classifier.predict(vec_tweet)) - 2

    def get_sentiment_of_text_list(self, texts) -> List[float]:
        res = []
        for text in texts:
            vec_tweet = self.vectorizer.transform([self.preprocess_text(text)])
            res.append(self.classifier.predict(vec_tweet))
        return [int(e) - 2 for e in res]

    def get_average_sentiment_of_text_list(self, texts) -> float:
        res = []
        for text in texts:
            vec_tweet = self.vectorizer.transform([self.preprocess_text(text)])
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
        tweets_text = tweets["text"]
        tweets_sentiment = tweets["sentiment"]

        # convert the labels to integers ("positive" -> 3, "neutral" -> 2, "negative" -> 1)
        labels = [3 if label == "positive" else 2 if label == "neutral" else 1 for label in tweets_sentiment]

        # use a TfidfVectorizer to convert the text to numerical features
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(map(lambda t: self.preprocess_text(t), tweets_text))

        # train a SGDClassifier model on the training data
        classifier = SGDClassifier()
        classifier.fit(X, labels)

        joblib.dump(classifier, self.path_to_model + "classifier" + ".joblib")
        joblib.dump(vectorizer, self.path_to_model + "vectorizer" + ".joblib")
        self.did_train = True

    def accuracy(self):
        # Load the test data
        tweets = pd.read_csv(self.path_to_test_data)
        tweets.dropna(inplace=True)
        tweets_text = tweets["text"]
        tweets_sentiment = tweets["sentiment"]

        # Convert the test labels to integers
        true_labels = [3 if label == "positive" else 2 if label == "neutral" else 1 for label in tweets_sentiment]

        # Transform the test data using the vectorizer
        X_test = self.vectorizer.transform(map(lambda t: self.preprocess_text(t), tweets_text))

        # Predict the sentiment of the test data using the classifier
        predicted_labels = self.classifier.predict(X_test)

        # Calculate the accuracy of the classifier
        return accuracy_score(true_labels, predicted_labels)

    def recall(self):
        # Load the test data
        tweets = pd.read_csv(self.path_to_test_data)
        tweets.dropna(inplace=True)
        tweets_text = tweets["text"]
        tweets_sentiment = tweets["sentiment"]

        # Convert the test labels to integers
        true_labels = [3 if label == "positive" else 2 if label == "neutral" else 1 for label in tweets_sentiment]

        # Transform the test data using the vectorizer
        X_test = self.vectorizer.transform(map(lambda t: self.preprocess_text(t), tweets_text))

        # Predict the sentiment of the test data using the classifier
        predicted_labels = self.classifier.predict(X_test)

        # Calculate the recall of the classifier
        return recall_score(true_labels, predicted_labels, average='macro')

    def f1_score(self):
        # Load the test data
        tweets = pd.read_csv(self.path_to_test_data)
        tweets.dropna(inplace=True)
        tweets_text = tweets["text"]
        tweets_sentiment = tweets["sentiment"]

        # Convert the test labels to integers
        true_labels = [3 if label == "positive" else 2 if label == "neutral" else 1 for label in tweets_sentiment]

        # Transform the test data using the vectorizer
        X_test = self.vectorizer.transform(map(lambda t: self.preprocess_text(t), tweets_text))

        # Predict the sentiment of the test data using the classifier
        predicted_labels = self.classifier.predict(X_test)

        # Calculate the f1 score of the classifier
        return f1_score(true_labels, predicted_labels, average='macro')
