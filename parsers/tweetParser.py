import json
import datetime
import time
from lib import fileController
from database import mongoController
from parsers import userParser

# Parses tweets into tweet objects
class tweetParser():

    # Takes initial tweet input from Streamer and creates a list of tweets
    # Input - Tweet object returned from API
    # Output - List of tweet objects
    def parse_stream_tweet_chain(self, tweet):
        json_tweet = json.loads(tweet)
        parsed_tweets = self.parse_tweets([], json_tweet)
        return parsed_tweets

    # Takes initial tweet input from REST API and creates a list of tweets
    # Input - Tweet object returned from API
    # Output - List of tweet objects
    def parse_rest_tweet_chain(self, tweets):
        parsed_tweets = []
        # Parse each API object into JSON then create list of tweet objects
        for tweet in tweets:
            temp = json.dumps(tweet._json)
            json_tweet = json.loads(temp)
            parsed_tweets.append(self.parse_tweets([], json_tweet))
        if len(parsed_tweets) > 0:
            return [x for x in parsed_tweets if x is not None]

    # Recursively create final tweet objects to be inserted into the db
    # Input - Empty list, API tweet object
    # Output - List of tweet objects
    def parse_tweets(self, final_tweets_list, json_tweet):
        print("PARSING TWEET")
        file_controller = fileController.fileController()
        database = mongoController.mongoController()

        # skip if repeated tweet
        if not database.tweets.get_tweet_exists(json_tweet['user']['id'], json_tweet['id']):
            # if user not in db - add them
            user = database.users.get_user_with_id(json_tweet['user']['id'])
            if not user:
                self.create_new_user(database, json_tweet['user'])

            # create if not a retweet
            if not 'retweeted_status' in json_tweet:
                mongo_tweet = self.mongo_tweet_structure(json_tweet)

                # parse the quoted tweet if exists
                if 'quoted_status' in json_tweet:
                    self.parse_tweets(final_tweets_list, json_tweet['quoted_status'])

                final_tweets_list.append(mongo_tweet)
            # if it is a retweet get the original tweet and parse
            else:
                self.parse_tweets(final_tweets_list, json_tweet['retweeted_status'])
                retweet_line = str(json_tweet['retweeted_status']['id']) + ':' + str(datetime.date.today())
                file_controller.append_one_line("data/retweets.txt", retweet_line)

        return final_tweets_list

    # Create the tweet object
    # Input - API Tweet json object
    # Output - Database tweet object
    def mongo_tweet_structure(self, json_tweet):
        mongo_tweet = {
            "idd": json_tweet['id'],
            "created_at": json_tweet['created_at'],
            "processed_at": str(datetime.datetime.now()),
            "text": self.parse_text(json_tweet),
            "user": json_tweet['user']['id'],
            "geo": json_tweet['geo'],
            "coordinates": json_tweet['coordinates'],
            "place": json_tweet['place'],
            "quote_count": self.parse_quote_count(json_tweet),
            "reply_count": self.parse_reply_count(json_tweet),
            "retweet_count": json_tweet['retweet_count'],
            "favorite_count": json_tweet['favorite_count'],
            "hashtags": self.parse_hashtags(json_tweet['entities']['hashtags'])
        }
        # Add reply information if appliciable
        if not json_tweet['in_reply_to_status_id'] == None:
            mongo_tweet['response_status'] = json_tweet['in_reply_to_status_id']
            mongo_tweet['response_user'] = json_tweet['in_reply_to_user_id']
        # Add quote information if appliciable
        if 'quoted_status' in json_tweet:
            mongo_tweet['quote_status'] = json_tweet['quoted_status']['id']
            mongo_tweet['quote_user'] = json_tweet['quoted_status']['user']['id']

        return mongo_tweet

    # Parse a user if not already in database
    # Insert the user into the database
    def create_new_user(self, database, user):
        file_controller = fileController.fileController()
        user_parser = userParser.userParser()
        parsed_user = user_parser.parse_user(user)

        database.users.insert_a_user(parsed_user)
        file_controller.append_one_line("data/users.txt", user['id'])

    # Extract user ids from mentions list
    # Input - Tweet mentions property
    # Output - List of user id's - one for each mention
    def parse_mentions(self, mentions):
        all_mentions = []
        for mention in mentions:
            all_mentions.append(mention['id_str'])
        return all_mentions

    # Extract hashtags from hashtag list
    # Input - Tweet hashtags property
    # Output - List of hashtags
    def parse_hashtags(self, hashtags):
        all_hashtags = []
        for hashtag in hashtags:
            all_hashtags.append(hashtag['text'])
        return all_hashtags

    # Extract full tweet if >140 characters
    def parse_text(self, tweet):
        if('extended_tweet' in tweet):
            return tweet['extended_tweet']['full_text']
        else:
            return tweet['text']

    # Returns number of times tweet quoted
    # Input - Tweet API
    # Output - Number of times quote tweeted or 'False' if none
    def parse_quote_count(self, tweet):
        if('quote_count' in tweet):
            return tweet['quote_count']
        else:
            return False

    # Returns number of times tweet replied to
    # Input - Tweet API
    # Output - Number of times tweet replied too or 'False' if none
    def parse_reply_count(self, tweet):
        if('reply_count' in tweet):
            return tweet['reply_count']
        else:
            return False
