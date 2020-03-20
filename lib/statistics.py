from database import mongoController

# Calculates basic statistics for given data sets
class statistics():

    # Calculates total tweets overall
    def total_tweets(self):
        database = mongoController.mongoController()
        all_tweets = database.tweets.get_all_tweets()
        total = 0
        # loop over tweets set for each user
        for tweets in all_tweets:
            # loop over each tweet for current user
            for tweet in tweets['tweets']:
                total = total + 1
        return total

    # Calculates total overall tweets for a group
    def total_tweets_group(self, group):
        database = mongoController.mongoController()
        all_tweets = database.tweets.get_all_tweets()
        total = 0
        # loop over tweets set for each user
        for tweets in all_tweets:
            # loop over each tweet for current user
            for tweet in tweets['tweets']:
                if 'group' in tweet and tweet['group'] == group:
                    total = total + 1
        return total

    def average_tweets_group(self):
        average = 0
        for i in range(20):
            average = average + self.total_tweets_group(i)
        return average/20

    # Loop through each group and find the group with the least tweets
    def smallest_tweets_group(self):
        smallest = 9999999
        group = 9999999
        for i in range(20):
            size = self.total_tweets_group(i)
            if size < smallest:
                smallest = size
                group = i
        return smallest, group

    # Loop through each group and find the group with the most tweets
    def largest_tweets_group(self):
        largest = 0
        group = 9999999
        for i in range(20):
            size = self.total_tweets_group(i)
            if size > largest:
                largest = size
                group = i
        return largest, group

    # Calculates total overall of some property
    # Property may be one of; retweets, followers, friends, hashtags, replies, quotes
    def total_retweets(self):
        database = mongoController.mongoController()
        all_tweets = database.tweets.get_all_tweets()
        total = 0

        for tweets in all_tweets:
            for tweet in tweets['tweets']:
                if 'retweets' in tweet:
                    total = total + len(tweet['retweets'])
        return total

    # Calculates total overall of some property for a given group
    # Property may be one of; retweets, followers, friends, hashtags, replies, quotes
    def total_retweets_group(self, group):
        database = mongoController.mongoController()
        all_tweets = database.tweets.get_all_tweets()
        total = 0

        for tweets in all_tweets:
            for tweet in tweets['tweets']:
                if 'group' in tweet and tweet['group'] == group and 'retweets' in tweet:
                    total = total + len(tweet['retweets'])
        return total

    # Loop through each group and find the group with the least amount of some property
    # Property may be one of; retweets, followers, friends, hashtags, replies, quotes
    def smallest_retweets_group(self):
        smallest = 9999999
        group = 9999999
        for i in range(20):
            size = self.total_retweets_group(i)
            if size < smallest:
                smallest = size
                group = i
            return smallest, group

    # Loop through each group and find the group with the most amount of some property
    # Property may be one of; retweets, followers, friends, hashtags, replies, quotes
    def largest_retweets_group(self):
        largest = 0
        group = 9999999
        for i in range(20):
            size = self.total_retweets_group(i)
            if size > largest:
                largest = size
                group = i
        return largest, group

    # Calculates total overall replies
    def total_replies(self):
        database = mongoController.mongoController()
        all_tweets = database.tweets.get_all_tweets()
        total = 0

        for tweets in all_tweets:
            for tweet in tweets['tweets']:
                if 'response_status' in tweet:
                    total = total + 1
        return total

    # Calculates total overall tweets which were replies for a given group
    def total_reply_group(self, group):
        database = mongoController.mongoController()
        all_tweets = database.tweets.get_all_tweets()
        total = 0

        for tweets in all_tweets:
            for tweet in tweets['tweets']:
                if 'group' in tweet and tweet['group'] == group and 'response_status' in tweet:
                    total = total + 1
        return total

    # Loop through each group and find the group with the least amount of some property
    # Property may be one of; retweets, followers, friends, hashtags, replies, quotes
    def smallest_reply_group(self):
        smallest = 9999999
        group = 9999999
        for i in range(20):
            size = self.total_reply_group(i)
            if size < smallest:
                smallest = size
                group = i
            return smallest, group

    # Loop through each group and find the group with the most amount of some property
    # Property may be one of; retweets, followers, friends, hashtags, replies, quotes
    def largest_reply_group(self):
        largest = 0
        group = 9999999
        for i in range(20):
            size = self.total_reply_group(i)
            if size > largest:
                largest = size
                group = i
        return largest, group

    # Calculates total overall quotes
    def total_quotes(self):
        database = mongoController.mongoController()
        all_tweets = database.tweets.get_all_tweets()
        total = 0

        for tweets in all_tweets:
            for tweet in tweets['tweets']:
                if 'quote_status' in tweet:
                    total = total + 1
        return total

    # Calculates total overall tweets which were quoted for a given group
    def total_quote_group(self, group):
        database = mongoController.mongoController()
        all_tweets = database.tweets.get_all_tweets()
        total = 0

        for tweets in all_tweets:
            for tweet in tweets['tweets']:
                if 'group' in tweet and tweet['group'] == group and 'quote_status' in tweet:
                    total = total + 1
        return total

    # Loop through each group and find the group with the least amount of some property
    # Property may be one of; retweets, followers, friends, hashtags, replies, quotes
    def smallest_quote_group(self):
        smallest = 9999999
        group = 9999999
        for i in range(20):
            size = self.total_quote_group(i)
            if size < smallest:
                smallest = size
                group = i
            return smallest, group

    # Loop through each group and find the group with the most amount of some property
    # Property may be one of; retweets, followers, friends, hashtags, replies, quotes
    def largest_quote_group(self):
        largest = 0
        group = 9999999
        for i in range(20):
            size = self.total_quote_group(i)
            if size > largest:
                largest = size
                group = i
        return largest, group
