from tweepy.streaming import StreamListener
from tweepy import Stream
from API import twitterAuthenticater
from parsers import tweetParser, userParser
from database import mongoController
import sys
import linecache

# Manages official twitter Stream APIs
class TwitterStreamer():

    def __init__(self):
        self.twitter_authenticater = twitterAuthenticater.TwitterAuthenticater()

    def stream_tweets(self, hash_tag_list):
        listener = TwitterListener()
        auth = self.twitter_authenticater.authenticate_twitter_app()
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)

    def stream_one_percent(self):
        stream.sample()

class TwitterListener(StreamListener):

    def __init__(self):
        self.tweet_parser = tweetParser.tweetParser()
        self.user_parser = userParser.userParser()
        self.database = mongoController.mongoController()

    # Retrieves the stream and passes to the processing function
    def on_data(self, data):
        print("STREAMER PROCESSING TWEET")
        self.process_data(data)

    # Process the tweets and users that are retrieved by the streamer
    def process_data(self, data):
        try:
            db_user = self.user_parser.parse_user_chain(data)
            self.database.users.insert_users(db_user)
            db_tweets = self.tweet_parser.parse_stream_tweet_chain(data)
            for db_tweet in db_tweets:
                self.database.tweets.insert_a_tweet(db_tweet)
            return True
        except BaseException as e:
            print("Error : ", str(e))
            self.PrintException()
        return True

    def on_error(self, status):
        if status == 420:
            return False
        print(status)

    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
