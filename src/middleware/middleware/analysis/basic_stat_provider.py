from middleware.analysis.tweet_provider import TweetProvider

class BasicStatProvider:
    def __init__(self) -> None:
        self.tweet_provider = TweetProvider()