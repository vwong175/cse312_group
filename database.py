from pymongo import MongoClient
#client = MongoClient('localhost', 27017)   #If you want to test locally
client = MongoClient('mongo')                #If you want to test with docker
db = client["userInfo"]
users = db["users"]
rank = db["rank"] # rank in {"username", rank#} format
