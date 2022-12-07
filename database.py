from pymongo import MongoClient
#client = MongoClient('localhost', 27017)   #If you want to test locally
client = MongoClient('mongo')                #If you want to test with docker
db = client["userInfo"]
users = db["users"]
rank = db["rank"] # rank in {"username", rank#} format

users.delete_many({})
#sample user data
import bcrypt
import uuid
salt = bcrypt.gensalt()
user = {
            "_id": uuid.uuid4().hex,
            "username": "someone",
            "email": "123456@gmail.com",
            "salt": salt,
            "password": bcrypt.hashpw("123456789".encode(), salt),
            "wins": 78,
            "played": 126
        }

users.insert_one(user)

salt1 = bcrypt.gensalt()
user1 = {
            "_id": uuid.uuid4().hex,
            "username": "someone1",
            "email": "654321@gmail.com",
            "salt": salt1,
            "password": bcrypt.hashpw("123456789".encode(), salt),
            "wins": 52,
            "played": 74
        }

users.insert_one(user1)