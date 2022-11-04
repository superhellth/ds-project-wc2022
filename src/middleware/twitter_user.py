import tweepy


class User:
    """A class representing a twitter user. Stores all available data concerning the user. Fetches data on init"""

    def __init__(self, user_id):
        # Gather user data from the twitter api
        token_file = open('../twitter-api-bearer-token.txt',
                          'r', encoding="utf_8")
        bearer_token = token_file.readline()
        twitter_client = tweepy.Client(bearer_token=bearer_token)
        user = twitter_client.get_user(id=user_id, user_fields=["created_at", "description", "entities", "location",
                                                                "pinned_tweet_id", "profile_image_url", "protected",
                                                                "public_metrics", "url", "verified", "withheld"]).data

        # Assign attributes
        self.created_at = user["created_at"]
        self.description = user["description"]
        self.entities = user["entities"]
        self.id = user["id"]
        self.location = user["location"]
        self.name = user["name"]
        self.pinned_tweet_id = user["pinned_tweet_id"]
        self.profile_image_url = user["profile_image_url"]
        self.protected = user["protected"]
        self.public_metrics = user["public_metrics"]
        self.url = user["url"]
        self.username = user["username"]
        self.verified = user["verified"]

    def get_as_json(self):
        """Returns the author as a json object"""
        return {
            "created_at": self.created_at,
            "description": self.description,
            "entities": self.entities,
            "id": self.id,
            "location": self.location,
            "name": self.name,
            "pinned_tweet_id": self.pinned_tweet_id,
            "profile_image_url": self.profile_image_url,
            "protected": self.protected,
            "public_metrics": self.public_metrics,
            "url": self.url,
            "username": self.username,
            "verified": self.verified
        }

    # Getter
    def get_created_at(self):
        """Return the creation date of the user account"""
        return self.created_at

    def get_description(self):
        """Return the description of the user"""
        return self.description

    def get_entities(self):
        """Return the entities of the user description"""
        return self.entities

    def get_id(self):
        """Return user id"""
        return self.id

    def get_location(self):
        """Returns the users location"""
        return self.location

    def get_name(self):
        """Return the user's full name"""
        return self.name

    def get_pinned_tweet_id(self):
        """Return the id of the pinned tweet of the user if it exists"""
        return self.pinned_tweet_id

    def get_profile_image_url(self):
        """Return url of the user's profile image"""
        return self.profile_image_url

    def is_protected(self):
        """Return wether the user account is set to private or not"""
        return self.protected

    def get_public_metrics(self):
        """Return the user's public metrics"""
        return self.public_metrics

    def get_url(self):
        """Return the url of the user account"""
        return self.url

    def get_username(self):
        """Return the @username of the user"""
        return self.username

    def is_verified(self):
        """Returns true if user is verified, else false"""
        return self.verified
