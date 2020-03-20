from database import mongoTweets, mongoUsers, mongoRetweets, mongoFollowers, mongoFriends
import pymongo
import json

# Controller for each type of database interaction
class mongoController():

    ### HIGH LEVEL CONTROLLER CONTAINERS ###
    def __init__(self):
        self.client = pymongo.MongoClient('localhost',27017)
        self.database = self.client["twitter"]
        self.tweets = mongoTweets.mongoTweets(self.database)
        self.users = mongoUsers.mongoUsers(self.database)
        self.retweets = mongoRetweets.mongoRetweets(self.database)
        self.followers = mongoFollowers.mongoFollowers(self.database)
        self.friends = mongoFriends.mongoFriends(self.database)
