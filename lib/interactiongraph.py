from database import mongoController

# @TODO ALL FUNCTIONS HERE NEED TO BE OPTIMIZED
## Functions here create corrosponding interaction graphs
class interactiongraph():

    def retweets_length(self):
        return len(self.retweets())

    # Iterates through each user and lists which users they have retweeted and how many times
    # Returns a dictonary of all users and the users they have retweeted with the quantity
    def retweets(self):
        database = mongoController.mongoController()
        users = database.users.get_all_users()

        retweet_map = {}
        for user in users:
            if 'tweets' in user:
                for tweet in user['tweets']:
                    if 'retweets' in tweet:
                        for retweet in tweet['retweets']:
                            for ind_retweets in retweet['retweets']:
                                if not ind_retweets['user'] in retweet_map:
                                    retweet_map[ind_retweets['user']] = {user['idd']: 1}
                                else:
                                    temp = retweet_map[ind_retweets['user']]
                                    if user['idd'] in temp:
                                        temp.update({ user['idd']: temp[user['idd']] + 1 })
                                    else:
                                        temp[user['idd']] = 1
        # print(retweet_map)
        return retweet_map

    # Iterates through each user for a given group and lists which users they have retweeted and how many times
    # Returns a dictonary of all users and the users they have retweeted with the quantity
    def retweets_group(self, group):
        database = mongoController.mongoController()
        users = database.users.get_all_users()

        retweet_map = {}
        for user in users:
            if 'tweets' in user:
                for tweet in user['tweets']:
                    if 'retweets' in tweet:
                        if 'group' in tweet and tweet['group'] == group:
                            for retweet in tweet['retweets']:
                                for ind_retweets in retweet['retweets']:
                                    if not ind_retweets['user'] in retweet_map:
                                        retweet_map[ind_retweets['user']] = {user['idd']: 1}
                                    else:
                                        temp = retweet_map[ind_retweets['user']]
                                        if user['idd'] in temp:
                                            temp.update({ user['idd']: temp[user['idd']] + 1 })
                                        else:
                                            temp[user['idd']] = 1
        # print(retweet_map)
        return retweet_map

    def quotes_length(self):
        return len(self.quotes())

    # Iterates through each user and lists which users they have quoted and how many times
    # Returns a dictonary of all users and the users they have quuoted with the quantity
    def quotes(self):
        database = mongoController.mongoController()
        users = database.users.get_all_users()

        quote_map = {}
        for user in users:
            if 'tweets' in user:
                for tweet in user['tweets']:
                    if 'quote_status' in tweet:
                        if not user['idd'] in quote_map:
                            quote_map[user['idd']] = { tweet['quote_user']: 1 }
                        else:
                            temp = quote_map[user['idd']]
                            if tweet['quote_user'] in temp:
                                temp.update({ tweet['quote_user']: temp[tweet['quote_user']] + 1 })
                            else:
                                temp[tweet['quote_user']] = 1
        # print(quote_map)
        return quote_map

    # Iterates through each user for a given group and lists which users they have quoted and how many times
    # Returns a dictonary of all users and the users they have quuoted with the quantity
    def quotes_group(self, group):
        database = mongoController.mongoController()
        users = database.users.get_all_users()

        quote_map = {}
        for user in users:
            if 'tweets' in user:
                for tweet in user['tweets']:
                    if 'quote_status' in tweet:
                        if 'group' in tweet and tweet['group'] == group:
                            if not user['idd'] in quote_map:
                                quote_map[user['idd']] = { tweet['quote_user']: 1 }
                            else:
                                temp = quote_map[user['idd']]
                                if tweet['quote_user'] in temp:
                                    temp.update({ tweet['quote_user']: temp[tweet['quote_user']] + 1 })
                                else:
                                    temp[tweet['quote_user']] = 1
        # print(quote_map)
        return quote_map

    # Iterates through each user and lists which users they have replied to and how many times
    # Returns a dictonary of all users and the users they have replied to with the quantity
    def replies(self):
        database = mongoController.mongoController()
        users = database.users.get_all_users()

        reply_map = {}
        for user in users:
            if 'tweets' in user:
                for tweet in user['tweets']:
                    if 'response_status' in tweet:
                        if not user['idd'] in reply_map:
                            reply_map[user['idd']] = { tweet['response_user']: 1 }
                        else:
                            temp = reply_map[user['idd']]
                            if tweet['response_user'] in temp:
                                temp.update({ tweet['response_user']: temp[tweet['response_user']] + 1 })
                            else:
                                temp[tweet['response_user']] = 1
        # print(reply_map)
        return reply_map

    # Iterates through each user for a given group and lists which users they have replied to and how many times
    # Returns a dictonary of all users and the users they have replied to with the quantity
    def replies_group(self, group):
        database = mongoController.mongoController()
        users = database.users.get_all_users()

        reply_map = {}
        for user in users:
            if 'tweets' in user:
                for tweet in user['tweets']:
                    if 'response_status' in tweet:
                        if 'group' in tweet and tweet['group'] == group:
                            if not user['idd'] in reply_map:
                                reply_map[user['idd']] = { tweet['response_user']: 1 }
                            else:
                                temp = reply_map[user['idd']]
                                if tweet['response_user'] in temp:
                                    temp.update({ tweet['response_user']: temp[tweet['response_user']] + 1 })
                                else:
                                    temp[tweet['response_user']] = 1
        # print(reply_map)
        return reply_map

    # Iterates through each user and lists which hashtags they share with other users
    # Returns a dictonary of all users and the users they have shared hashtags with
    def hashtags(self):
        database = mongoController.mongoController()
        users = database.users.get_all_users()
        usable_users = []

        hashtag_map = {}
        for user in users:
            if 'tweets' in user:
                usable_users.append(user)

        for i, user in enumerate(usable_users):
            for tweet in user['tweets']:
                for hashtag in tweet['hashtags']:
                    if not hashtag in hashtag_map:
                        hashtag_map[hashtag] = { tweet['user']: 1 }
                    else:
                        temp = hashtag_map[hashtag]
                        if tweet['user'] in temp:
                            temp.update({ tweet['user']: temp[tweet['user']] + 1 })
                        else:
                            temp[tweet['user']] = 1
        return hashtag_map

    # Iterates through each user for a given group and lists which hashtags they share with other users
    # Returns a dictonary of all users and the users they have shared hashtags with
    def hashtags_groups(self, group):
        database = mongoController.mongoController()
        users = database.users.get_all_users()

        hashtag_map = {}
        for user in users:
            if 'tweets' in user:
                for tweet in user['tweets']:
                    if 'group' in tweet and tweet['group'] == group:
                        for hashtag in tweet['hashtags']:
                            if not hashtag in hashtag_map:
                                hashtag_map[hashtag] = { tweet['user']: 1 }
                            else:
                                temp = hashtag_map[hashtag]
                                if tweet['user'] in temp:
                                    temp.update({ tweet['user']: temp[tweet['user']] + 1 })
                                else:
                                    temp[tweet['user']] = 1
        # print(hashtag_map)
        return hashtag_map

    def hashtags_length(self):
        return len(self.hashtags_user())

    def hashtags_user(self, group):
        if group == "all":
            hashtag_map = self.hashtags()
        else:
            hashtag_map = self.hashtags_groups(group)
        user_map = {}
        for i in hashtag_map.values():
            for z in i:
                users = i.copy()
                users.pop(z, None)
                if not z in user_map:
                    user_map[z] = {}
                for user in users:
                    if not user in user_map[z]:
                        user_map[z][user] = 1
                    else:
                        user_map[z].update({ user: user_map[z][user] + 1 })
        # print(user_map)
        return user_map
