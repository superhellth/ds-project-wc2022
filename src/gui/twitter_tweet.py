import twitter_user

class Tweet:

    def __init__(self, tweet_data):
        self.id = tweet_data.id
        self.author = twitter_user.User(tweet_data.author_id)
        self.text = tweet_data.text
        self.created_at = tweet_data.created_at
        self.public_metrics = tweet_data.public_metrics

    def print(self):
        print(f"tweet_id: {self.id}")
        print(f"text: {self.text}")
        print(f"author_id: {self.author.id}")
        print(f"author name: {self.author.name}")
        print(f"author username: {self.author.username}")
        print(f"author metrics: {self.author.public_metrics}")
        print(f"created_at: {self.created_at}")
        print(f"metrics: {self.public_metrics}")
        print("\n")

    def get_as_es_doc(self):
        tweet_doc = {
            "tweet_id": self.id,
            "author": {
                "id": self.id,
                "name": self.author.name,
                "username": self.author.username,
                "follower_count": self.author.public_metrics["followers_count"]
            },
            "text": self.text,
            "created_at": self.created_at,
            "like_count": self.public_metrics["like_count"],
            "retweet_count": self.public_metrics["retweet_count"],
            "reply_count": self.public_metrics["reply_count"]
        }
        return tweet_doc