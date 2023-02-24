from middleware.tweet_management import twitter_user


class Tweet:
    """A class to store and manage all available data about a tweet."""

    def __init__(self, raw_data, is_es_doc=False):
        if is_es_doc:
            tweet = raw_data["_source"]
            user = tweet.get("author", None)
        else:
            tweet = raw_data["data"]
            user = raw_data["includes"]["users"][0]

        self.attachments = tweet.get("attachments", None)
        self.author = twitter_user.User(user)
        self.context_annotations = tweet.get("context_annotations", None)
        self.conversation_id = tweet.get("conversation_id", None)
        self.created_at = tweet.get("created_at", None)
        self.edit_controls = tweet.get("edit_controls", None)
        self.edit_history_tweet_ids = tweet.get("edit_history_tweet_ids", None)
        self.entities = tweet.get("entities", None)
        self.id = tweet.get("id", None)
        self.in_reply_to_user_id = tweet.get("in_reply_to_user_id", None)
        self.lang = tweet.get("lang", None)
        self.possibly_sensitive = tweet.get("possibly_sensitive", None)
        self.public_metrics = tweet.get("public_metrics", None)
        self.referenced_tweets = tweet.get("referenced_tweets", None)
        self.reply_settings = tweet.get("reply_settings", None)
        self.source = tweet.get("source", None)
        self.text = tweet.get("text", None)
        self.withheld = tweet.get("withheld", None)

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

    def get_attachments(self):
        return self.attachments

    def get_author(self):
        return self.author

    def get_context_annotations(self):
        return self.context_annotations

    def get_conversation_id(self):
        return self.conversation_id

    def get_created_at(self):
        return self.created_at

    def get_edit_controls(self):
        return self.edit_controls

    def get_edit_history_tweet_ids(self):
        return self.edit_history_tweet_ids

    def get_entities(self):
        return self.entities

    def get_id(self):
        return self.id

    def get_in_reply_to_user_id(self):
        return self.in_reply_to_user_id

    def get_lang(self):
        return self.lang

    def get_possibly_sensitive(self):
        return self.possibly_sensitive

    def get_public_metrics(self):
        return self.public_metrics

    def get_referenced_tweets(self):
        return self.referenced_tweets

    def get_reply_settings(self):
        return self.reply_settings

    def get_source(self):
        return self.source

    def get_text(self):
        return self.text

    def get_withheld(self):
        return self.withheld
