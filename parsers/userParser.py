from lib import fileController
import json
import datetime

# Parses tweets to create user objects
class userParser():

    # Takes initial tweet input and creates a list of users taken from the tweet
    # Input - Tweet object returned from API
    # Output - List of user objects
    def parse_user_chain(self, tweet):
        json_user = json.loads(tweet)
        parsed_users = self.parse_users([], json_user)
        return parsed_users

    # Recursively create final user objects to be inserted into db
    # Set followers & friends to be retrieved for this account
    # Input - Empty list, API tweet object
    # Output - List of user objects
    def parse_users(self, list, json_user):
        print("PARSING USER")
        # sometimes the rate limit is sent instead of real data
        if not 'user' in json_user:
            return list

        # Create user object
        file_controller = fileController.fileController()
        list.append({
            "idd": json_user['user']['id'],
            "screen_name": json_user['user']['screen_name'],
            "location": json_user['user']['location'],
            "verified": json_user['user']['verified'],
            "followers_count": json_user['user']['followers_count'],
            "friends_count": json_user['user']['friends_count'],
            "favourites_count": json_user['user']['favourites_count'],
            "statuses_count": json_user['user']['statuses_count'],
            "created_at": json_user['user']['created_at'],
            "geo_enabled": json_user['user']['geo_enabled'],
        })

        # If tweet was a retweet then parse the retweet user
        if 'retweeted_status' in json_user:
            self.parse_users(list, json_user['retweeted_status'])

        # If the tweet quoted another status then parse the quote user
        if 'quoted_status' in json_user:
            self.parse_users(list, json_user['quoted_status'])

        # Insert user id into followers & friends file to be processed by REST APIs
        follower_line = str(json_user['user']['id']) + ':' + str(datetime.date.today())
        file_controller.append_one_line("data/followers.txt", follower_line)
        friend_line = str(json_user['user']['id']) + ':' + str(datetime.date.today())
        file_controller.append_one_line("data/friends.txt", friend_line)

        return list

    # @TODO - deprecate
    # a single user should be parsed as many users and take result[0] as response
    def parse_user(self, json_user):
        file_controller = fileController.fileController()
        return {
            "idd": json_user['id'],
            "screen_name": json_user['screen_name'],
            "location": json_user['location'],
            "verified": json_user['verified'],
            "followers_count": json_user['followers_count'],
            "friends_count": json_user['friends_count'],
            "favourites_count": json_user['favourites_count'],
            "statuses_count": json_user['statuses_count'],
            "created_at": json_user['created_at'],
            "geo_enabled": json_user['geo_enabled'],
        }

        if 'retweeted_status' in json_user:
            self.parse_users(list, json_user['retweeted_status'])

        if 'quoted_status' in json_user:
            self.parse_users(list, json_user['quoted_Status'])

        follower_line = str(json_user['user']['id']) + ':' + str(datetime.date.today())
        file_controller.append_one_line("data/followers.txt", follower_line)
        friend_line = str(json_user['user']['id']) + ':' + str(datetime.date.today())
        file_controller.append_one_line("data/friends.txt", friend_line)

        return list
