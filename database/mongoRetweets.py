import pymongo
from database import mongoController

# Manages interactions with the database for retweet objects
class mongoRetweets:

    def __init__(self, database):
        self.users_table = database["users"]

    def insert_retweets(self, ids, retweets):
        for i in retweets["retweets"]:
            if(self.get_retweet_exists(i['user'], i['idd'])):
                retweets.remove(i)
        if(len(retweets["retweets"]) == 0):
            return False
        else:
            self.insert_a_retweet(ids, retweets)
        return True

    def insert_a_retweet(self, tweet_id, retweet):
        query = { "tweets.idd": int(tweet_id) }
        action = { "$push": { "tweets.$.retweets": retweet}}
        self.users_table.update_one(query, action)

    def insert_many_retweets(self, retweets):
        for retweet in retweets:
            self.insert_a_retweet(retweet)

    def get_retweet_with_id(self, user_id, id):
        retweet = self.users_table.find_one({"idd": user_id, "retweet.idd": id})
        if retweet:
            return retweet
        return False

    def get_all_retweets(self):
        retweets = self.users_table.find({}, { "retweets": 1 })
        all_retweets = []
        for retweet in retweets:
            all_retweets.append(retweet)
        return [x for x in all_retweets if 'retweets' in x]

    def remove_retweet_with_id(self, user_id, id):
        self.users_table.delete_one({"idd": user_id})

    def get_retweet_exists(self, user_id, id):
        retweet = self.users_table.find_one({"idd": user_id, "retweets.idd": id})
        if retweet:
            return True
        else:
            return False
