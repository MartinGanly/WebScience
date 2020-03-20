from parsers import retweetParser, tweetParser, followerParser, userParser
from lib import fileController
from database import mongoController
import time
import datetime

# Controls the main loop of each API service
class restController():

    def __init__(self, rest_client):
        self.rest_client = rest_client
        self.file_controller = fileController.fileController()
        self.retweet_parser = retweetParser.retweetParser()
        self.tweet_parser = tweetParser.tweetParser()
        self.follower_parser = followerParser.followerParser()

    # Execution of the twitter retweet API calls.
    # Retrieves a tweet ID from file
    # Parses the API result into a retweet object
    # Inserts the retweet object into the tweet in the database
    def retweet_loop(self):
        database = mongoController.mongoController()
        while(True):
            print("REST API PROCESSING RETWEETS")
            # get the tweet id from file
            tweet_id_line = self.file_controller.get_and_remove_first_line("data/retweets.txt")
            if(tweet_id_line == False):
                time.sleep(60 * 2)
                continue

            # calculate the difference between today and the date user was added to file
            split_tweet_line = tweet_id_line.split(':')
            date_difference = self.calculate_days_diff_from_today(split_tweet_line[1])

            # if ready to be processed
            # parse and add to tweet database object
            if(date_difference.days > 1):
                retweets = self.rest_client.get_retweets(split_tweet_line[0])
                parsed_retweets = self.retweet_parser.parse_retweet_chain(split_tweet_line[0], retweets)
                database.retweets.insert_retweets(split_tweet_line[0], parsed_retweets)
            # else re-add tweet id to bottom of file
            else:
                self.file_controller.append_one_line("data/retweets.txt", tweet_id_line)

    # Execution of the twitter followers API calls.
    # Retrieves a tweet ID from file
    # Parses the API result into a follower object. Uses both follower_id API and follower API
    # Inserts the follower object into the tweet in the database
    def followers_loop(self):
        database = mongoController.mongoController()
        switch = 0
        while(True):
            print("REST API PROCESSING FOLLOWERS")
            # get the user id from file
            follower_id_line = self.file_controller.get_and_remove_first_line("data/followers.txt")
            if(follower_id_line == False):
                time.sleep(60 * 2)
                continue

            split_follower_id_line = follower_id_line.split(':')
            date_difference = self.calculate_days_diff_from_today(split_follower_id_line[1])

            if(date_difference.days > 1):
                # switch between both follower API's
                user = database.users.get_user_with_id(split_follower_id_line[0])
                if not 'followers' in user:
                    if(switch % 2 == 0):
                        followers = self.rest_client.get_followers(split_follower_id_line[0])
                        all_followers = self.follower_parser.parse_followers(followers)
                    else:
                        all_followers = self.rest_client.get_followers_ids(split_follower_id_line[0])

                    # insert followers to db
                    database.followers.insert_followers(split_follower_id_line[0], all_followers)

                    # calculate switch
                    if (switch) == 1:
                        switch = 0
                    else:
                        switch = switch + 1
            else:
                self.file_controller.append_one_line("data/followers.txt", follower_id_line)

    # Execution of the twitter friends API calls.
    # Retrieves a user ID from file
    # Parses the API result into a friends object
    # Inserts the friends object into the tweet in the database
    def friends_loop(self):
        database = mongoController.mongoController()
        while(True):
            print("REST API PROCESSING FRIENDS")
            # get user id from file
            friends_id_line = self.file_controller.get_and_remove_first_line("data/friends.txt")
            if(friends_id_line == False):
                time.sleep(60 * 2)
                continue

            split_friends_id_line = friends_id_line.split(":")
            date_difference = self.calculate_days_diff_from_today(split_friends_id_line[1])

            if(date_difference.days > 1):
                user = database.users.get_user_with_id(split_friends_id_line[0])
                if not 'friends' in user:
                    # get users friends and insert into db
                    friends = self.rest_client.get_friends_ids(friends_id_line[0])
                    database.friends.insert_friends(split_friends_id_line[0], friends)
            else:
                self.file_controller.append_one_line("data/friends.txt", friends_id_line)

    # Execution of the twitter timeline API calls.
    # Retrieves a user ID from file
    # Parses the API result into tweet objects
    # Inserts the tweet objects into the tweet in the database
    def timeline_loop(self):
        database = mongoController.mongoController()
        while(True):
            print("REST API PROCESSING USERS TIMELINE")
            # get the user id from file
            timeline_id_line = self.file_controller.get_and_remove_first_line("data/users.txt")
            if(timeline_id_line == False):
                time.sleep(60 * 2)
                continue

            tweets = self.rest_client.get_tweets_from_user(timeline_id_line)

            # parse and insert tweets
            parsed_tweets = self.tweet_parser.parse_rest_tweet_chain(tweets)
            if not parsed_tweets is None:
                for parsed_tweet in parsed_tweets:
                    if len(parsed_tweet) > 0:
                        database.tweets.insert_tweets(parsed_tweet)

    def calculate_days_diff_from_today(self, date):
        tweet_recorded_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        todays_date = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
        return todays_date - tweet_recorded_date
