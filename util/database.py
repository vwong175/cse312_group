from pymongo import MongoClient

mongoClient = MongoClient("mongo")
db = mongoClient["GroupProject"]
commentHistory = db["users"]

currentId = db["Ids"]
xsrfTokens = db["tokens"]