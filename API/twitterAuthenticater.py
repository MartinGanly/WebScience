from tweepy import OAuthHandler
from API import credentials

class TwitterAuthenticater:

    def __init__(self):
        pass

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        return auth
