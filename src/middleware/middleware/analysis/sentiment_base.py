from abc import ABC, abstractmethod
from typing import List, Tuple


class SentimentBase(ABC):
    def __init__(self, model_name: str, path_to_model: str = None, path_to_training_data: str = None,
                 path_to_test_data: str = None) -> None:
        self.did_train = False
        self.model_name = model_name
        self.path_to_model = path_to_model
        self.path_to_training_data = path_to_training_data
        self.path_to_test_data = path_to_test_data

    @abstractmethod
    def get_sentiment_of_text(self, text: str):
        pass

    @abstractmethod
    def get_sentiment_of_text_list(self, texts: List[str]):
        pass

    @abstractmethod
    def get_average_sentiment_of_text_list(self, texts: List[str]):
        pass

    @abstractmethod
    def get_sentiment_of_text_list_by_date(self, texts: List[Tuple[str, str]]):
        pass

    @abstractmethod
    def train_and_save_model(self):
        pass

    @abstractmethod
    def preprocess_text(self, text: str):
        pass
