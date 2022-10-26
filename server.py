import socketserver
from pymongo import MongoClient
import json
import random
import string


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):

        received_data = self.request.recv(2048)
        
        
        mongo_client = MongoClient('mongo')
        db = mongo_client["cse312_Project"]
        
        users_account = db["account"]
        

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()
