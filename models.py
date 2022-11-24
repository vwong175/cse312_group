import bcrypt
from flask import Flask, jsonify, request, session, redirect
from pymongo import MongoClient
# from server import users
import uuid

client = MongoClient('localhost', 27017) #Connect to the hostname 'mongo' as defined in the docker compose file
db = client["userInfo"]
users = db["users"]
rank = db["rank"] # rank in {"username", rank#} format

class User:

    def start_session(self, user):
        session['logged_in'] = True
        session['userid'] = user["_id"]
        return redirect('/profile/'+user["_id"])

    def signup(self):
        salt = bcrypt.gensalt()
        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "salt": salt,
            "password": bcrypt.hashpw(request.form.get('password').encode(),salt),
            "wins": 0,
            "played": 0
        }

        condition1 = users.find_one({"email": user['email']}) == None
        # Check for existing email address
        if condition1 == False:
            return jsonify({"failed": "Email address already in use"}), 400

        if request.form.get('password') != request.form.get('confirm_password'):
            return jsonify({"failed": "password are not the same"}), 400


        if users.insert_one(user):
            id = user["_id"]
            print(list(users.find()))
            # return redirect('/profile/'+id)

        return jsonify({"failed": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        userFound = users.find_one({"username": request.form.get('username')})

        if userFound and bcrypt.hashpw(request.form.get('password').encode(),userFound['salt']) == userFound['password']:
            return self.start_session(userFound)

        return jsonify({"failed": "Can't login due to wrong password or invalid email."}), 401