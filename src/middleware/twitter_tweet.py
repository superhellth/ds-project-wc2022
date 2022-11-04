import twitter_user


class Tweet:
    """A class to store and manage all available data about a tweet."""

    def __init__(self, tweet):
        self.attachments = tweet["attachments"]
        self.author = twitter_user.User(tweet["author_id"])
        self.context_annotations = tweet["context_annotations"]
        self.conversation_id = tweet["conversation_id"]
        self.created_at = tweet["created_at"]
        self.edit_controls = tweet["edit_controls"]
        self.edit_history_tweet_ids = tweet["edit_history_tweet_ids"]
        self.entities = tweet["entities"]
        self.id = tweet["id"]
        self.in_reply_to_user_id = tweet["in_reply_to_user_id"]
        self.lang = tweet["lang"]
        self.possibly_sensitive = tweet["possibly_sensitive"]
        self.public_metrics = tweet["public_metrics"]
        self.referenced_tweets = tweet["referenced_tweets"]
        self.reply_settings = tweet["reply_settings"]
        self.source = tweet["source"]
        self.text = tweet["text"]
        self.withheld = tweet["withheld"]

    def get_as_es_doc(self):
        """Returns the tweet object as a json object"""
        referenced_tweets = None
        if self.referenced_tweets is not None:
            referenced_tweets = []
            for referenced_tweet in self.referenced_tweets:
                referenced_tweets.append({
                    "type": referenced_tweet["type"],
                    "id": referenced_tweet["id"]
                })

        tweet_doc = {
            "attachments": self.attachments,
            "author": self.author.get_as_json(),
            "context_annotations": self.context_annotations,
            "conversation_id": self.conversation_id,
            "created_at": self.created_at,
            "edit_controls": self.edit_controls,
            "edit_history_tweet_ids": self.edit_history_tweet_ids,
            "entities": self.entities,
            "id": self.id,
            "in_reply_to_user_id": self.in_reply_to_user_id,
            "lang": self.lang,
            "possibly_sensitive": self.possibly_sensitive,
            "public_metrics": self.public_metrics,
            "referenced_tweets": referenced_tweets,
            "reply_settings": self.reply_settings,
            "source": self.source,
            "text": self.text,
            "withheld": self.withheld
        }
        return tweet_doc

    def get_id(self):
        """Returns the tweet id"""
        return self.id
