import pymongo
import json

# Manages interactions with the database for tweet objects
class mongoTweets():

    def __init__(self, database):
        self.users_table = database["users"]

    def insert_tweets(self, tweets):
        for i in tweets:
            if(self.get_tweet_exists(i['user'], i['idd'])):
                tweets.remove(i)
        if(len(tweets) == 0):
            return False
        else:
            self.insert_many_tweets(tweets)
        return True

    def insert_a_tweet(self, tweet):
        query = { "idd": tweet['user']}
        action = { "$push": { "tweets": tweet }}
        self.users_table.update_one(query, action)

    def insert_many_tweets(self, tweets):
        for tweet in tweets:
            self.insert_a_tweet(tweet)

    def get_tweet_with_id(self, tweet_id):
        tweet = self.users_table.find_one({"tweets.idd": tweet_id})
        if tweet:
            return tweet
        return False

    def get_tweet_text_with_id(self, tweet_id):
        tweet = self.users_table.find_one({"tweets.idd": tweet_id}, {"tweets.text": 1})
        if tweet:
            return tweet
        return False

    def get_all_tweets_from_user(self, user_id):
        tweets = self.users_table.find({ "idd": user_id }, { "tweets": 1 })
        all_tweets = []
        for tweet in tweets:
            all_tweets.append(tweet)
        return [x for x in all_tweets if 'tweets' in x]

    def get_all_tweets(self):
        tweets = self.users_table.find({}, { "tweets": 1 })
        all_tweets = []
        for tweet in tweets:
            all_tweets.append(tweet)
        return [x for x in all_tweets if 'tweets' in x]

    def get_all_tweets_text(self):
        tweets = self.users_table.find({}, { "tweets.text": 1 })
        all_tweets = []
        for tweet in tweets:
            all_tweets.append(tweet)
        return [x for x in all_tweets if 'tweets' in x]

    def insert_sentiment_to_tweet(self, tweet_id, sentiment):
        query = { "tweets.idd": int(tweet_id) }
        action = { "$push": { "tweets.$.sentiment": sentiment}}
        self.users_table.update_one(query, action)

    def insert_group_to_tweet(self, tweet_id, group):
        query = { "tweets.idd": int(tweet_id) }
        action = { "$set": { "tweets.$.group": int(group) }}
        self.users_table.update_one(query, action)

    def remove_tweet_with_id(self, user_id, id):
        self.users_table.delete_one({"idd": user_id, "tweets.idd": id})

    def get_tweet_exists(self, user_id, tweet_id):
        tweet = self.users_table.find_one({"idd": user_id, "tweets.idd": tweet_id})
        if tweet:
            return True
        return False
