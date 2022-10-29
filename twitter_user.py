import tweepy

class User:
    
    def __init__(self, user_id):
        token_file = open('token.txt','r')
        bearer_token = token_file.readline()
        twitter_client = tweepy.Client(bearer_token=bearer_token)
        user = twitter_client.get_user(id=user_id, user_fields=["public_metrics"])
        self.id = user.data.id
        self.name = user.data.name
        self.username = user.data.username
        self.public_metrics = user.data.public_metrics