from database import mongoController
from parsers import userParser
import json

# Parses followers into a list of user_id's which will be appended to the tweet
class followerParser():

    def __init__(self):
        self.user_parser = userParser.userParser()

    # Extracts the user id's from each follower of a given tweet
    # Input - followers API object 
    # Output - a list of all followers ids
    def parse_followers(self, followers):
        database = mongoController.mongoController()
        all_followers = []
        for follower in followers:
            # Parse into json
            temp = json.dumps(follower._json)
            json_follower = json.loads(temp)

            # does user exist? Create user if not
            user_exists = database.users.get_user_exists(json_follower['id'])
            if not user_exists:
                new_user = self.user_parser.parse_user(json_follower)
                database.users.insert_a_user(new_user)

            # user = database.users.get_user_with_id(json_follower['id'])
            all_followers.append(json_follower['id'])

        return all_followers
