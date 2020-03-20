from API import twitterAuthenticater
from tweepy import API
from tweepy import Cursor

# Manages official twitter REST API calls
# Waits for rate limit to reset when reached
class twitterClient():

    def __init__(self):
        self.auth = twitterAuthenticater.TwitterAuthenticater().authenticate_twitter_app()
        self.twitter_client = API(auth_handler=self.auth, wait_on_rate_limit=True)

    def get_tweets_from_user(self, twitter_user):
        tweets = []
        for i in range(5):
            results = self.twitter_client.user_timeline(twitter_user, page=i)
        for result in results:
            tweets.append(result)
        return tweets

    def get_friend_list(self):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends).items():
            friend_list.append(friend)
        return friend_list

    def get_retweets(self, tweet_id):
        return self.twitter_client.retweets(tweet_id)

    def get_followers(self, user_id):
        return self.twitter_client.followers('user_id'==user_id)

    def get_followers_ids(self, user_id):
        return self.twitter_client.followers_ids('user_id'==user_id)

    def get_friends_ids(self, user_id):
        return self.twitter_client.friends_ids('user_id'==user_id)

    def get_trending_list(self):
        trend_list = []
        trends = self.twitter_client.trends_place(44418)
        for trend in trends[0]['trends']:
            parsed_trend = self.parse_trend(trend['name'])
            trend_list.append(parsed_trend)
        return trend_list

    def get_limit_status(self):
        return self.twitter_client.rate_limit_status()

    def parse_trend(self, trend):
        if(trend[0] == '#'):
            return trend[1:]
        else:
            return trend
