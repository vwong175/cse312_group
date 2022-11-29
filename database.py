from pymongo import MongoClient

client = MongoClient('localhost', 27017) #Connect to the hostname 'mongo' as defined in the docker compose file
db = client["userInfo"]
users = db["users"]
rank = db["rank"] # rank in {"username", rank#} format