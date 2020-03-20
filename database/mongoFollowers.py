import pymongo

# Manages interactions with the database for follower objects
class mongoFollowers():

    def __init__(self, database):
        self.users_table = database["users"]

    def insert_followers(self, user_id, followers):
        for follower in followers:
            if(self.get_follower_exists(int(user_id), follower)):
                followers.remove(follower)
        if(len(followers) == 0):
            return False
        else:
            self.insert_many_followers(user_id, followers)
        return True

    def insert_a_follower(self, user_id, follower):
        query = { "idd": int(user_id) }
        action = { "$push": { "followers": follower }}
        self.users_table.update_one(query, action)

    def insert_many_followers(self, user_id, followers):
        for follower in followers:
            self.insert_a_follower(user_id, follower)

    def get_follower_with_id(self, user_id, follower_id):
        follower = self.users_table.find_one({"idd": user_id, "followers.idd": follower_id})
        if follower:
            return follower
        return False

    def get_all_followers_from_user(self, user_id):
        followers = self.users_table.find({ "idd": user_id }, { "followers": 1 })
        all_followers = []
        for follower in followers:
            all_followers.append(follower)
        return [x for x in all_followers if 'followers' in x]

    def get_all_followers(self):
        followers = self.users_table.find({}, { "followers": 1 })
        all_followers = []
        for follower in followers:
            all_followers.append(follower)
        return [x for x in all_followers if 'followers' in x]

    def remove_follower_with_id(self, user_id, follower_id):
        self.users_table.delete_one({"idd": user_id, "followers.idd": id})

    def get_follower_exists(self, user_id, follower_id):
        follower = self.users_table.find_one({"idd": user_id, "followers": follower_id})
        if follower:
            return True
        return False
