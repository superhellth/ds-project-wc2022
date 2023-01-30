from abc import ABC, abstractmethod


class SentimentBase(ABC):
    def __init__(self, model_name, path_to_model=None, path_to_training_data=None):
        self.did_train = False
        self.model_name = model_name
        self.path_to_model = path_to_model
        self.path_to_training_data = path_to_training_data

    @abstractmethod
    def get_sentiment_of_text(self, text):
        pass

    @abstractmethod
    def get_sentiment_of_text_list(self, texts):
        pass

    @abstractmethod
    def get_average_sentiment_of_text_list(self, texts):
        pass

    @abstractmethod
    def get_sentiment_of_text_list_by_date(self, texts):
        pass

    @abstractmethod
    def train_and_save_model(self):
        pass

    @abstractmethod
    def preprocess_text(self, text):
        """
        This is a private method that preprocesses text
        """
        # Code to preprocess text goes here
        pass
