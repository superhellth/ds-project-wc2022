class User:
    """A class representing a twitter user. Stores all available data concerning the user. Fetches data on init"""

    def __init__(self, user):
        if user is None:
            user = {}
        self.created_at = user.get("created_at", None)
        self.description = user.get("description", None)
        self.entities = user.get("entities", None)
        self.id = user.get("id", None)
        self.location = user.get("location", None)
        self.name = user.get("name", None)
        self.pinned_tweet_id = user.get("pinned_tweet_id", None)
        self.profile_image_url = user.get("profile_image_url", None)
        self.protected = user.get("protected", None)
        self.public_metrics = user.get("public_metrics", None)
        self.url = user.get("url", None)
        self.username = user.get("username", None)
        self.verified = user.get("verified", None)

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
