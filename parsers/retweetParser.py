from lib import fileController
from parsers import userParser
import json
import time
import datetime

# Parses tweets into retweet objects
class retweetParser():

    def __init__(self):
        self.user_parser = userParser.userParser()

    # Takes initial tweet input from API and creates a retweets object
    # Input - tweet id, Tweet object returned from API
    # Output - Retweet object with a string of the retweet text and a list of user informations
    def parse_retweet_chain(self, tweet_id, retweets):
        # Set up basic object
        parsed_retweets = {
            "text": "",
            "retweets": []
        }
        # Iterate through retweets and assign user information to list
        for retweet in retweets:
            temp = json.dumps(retweet._json)
            json_retweet = json.loads(temp)
            # if text hasn't been applied then take it (happens on first iteration)
            if(parsed_retweets["text"] == ""):
                parsed_retweets["text"] = json_retweet["text"]
            parsed_retweets["retweets"].append(self.parse_retweets(tweet_id, json_retweet))
        return parsed_retweets

    # Creates the retweet user information that is appended to the retweets list for a given tweet
    # Input - tweet id, retweet API object
    # Output - A single element of the retweet list which contains the user information
    def parse_retweets(self, tweet_id, json_retweet):
        file_controller = fileController.fileController()
        file_controller.append_one_line("data/users.txt", json_retweet['user']['id'])

        final_retweet = {
            "idd": json_retweet['id'],
            "user": json_retweet['user']['id'],
            "created_at": json_retweet['created_at'],
            "processed_at": str(datetime.datetime.now())
        }
        return final_retweet

    def parse_text(self, tweet):
        if(tweet['truncated']):
            return tweet['extended_tweet']['full_text']
        else:
            return tweet['text']
