import pymongo

# Manages interactions with the database for friend objects
class mongoFriends():

    def __init__(self, database):
        self.users_table = database["users"]

    def insert_friends(self, user_id, friends):
        query = { "idd": int(user_id) }
        action = { "$push": { "friends": friends } }
        self.users_table.update_one(query, action)

    def get_friends_with_id(self, friend_id):
        friend = self.users_table.find_one({ "idd": friend_id })
        if friend:
            return friend
        return False

    def get_all_friends(self, user_id):
        friends = self.users_table.find({ "idd": user_id }, { "friends": 1 })
        return friends

    def get_friend_exists(self, user_id, friend_id):
        friend = self.users_table.find_one({ "idd": user_id, "friends": friend_id})
        if friend:
            return True
        return False
