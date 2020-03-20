import pymongo
import json

# Manages interactions with the database for user objects
class mongoUsers():

    def __init__(self, database):
        self.user_table = database["users"]

    def insert_users(self, users):
        for user in users:
            if(self.get_user_exists(user['idd'])):
                users.remove(user)
        if(len(users) == 0):
            return False
        elif(len(users) == 1):
            self.insert_a_user(users[0])
        else:
            self.insert_many_users(users)

    def insert_a_user(self, user):
        self.user_table.insert_one(user)

    def insert_many_users(self, users):
        self.user_table.insert_many(users, ordered=False)

    def get_user_with_id(self, id):
        user = self.user_table.find_one({"idd": int(id)})
        if user:
            return user
        return False

    def get_all_users(self):
        all_users = []
        for user in self.user_table.find():
            all_users.append(user)
        return all_users

    def remove_user_with_id(self, id):
        self.user_table.delete_one({"idd": id})

    def remove_all_users(self):
        self.user_table.drop()

    def get_user_exists(self, id):
        result = self.user_table.find({"idd": id})
        if(result.count() == 0):
            return False
        else:
            return True
