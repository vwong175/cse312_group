import bcrypt
from flask import Flask, jsonify, request, session, redirect
from server import db
import uuid


class User:

    def start_session(self, user):
        session['logged_in'] = True
        session['user'] = {user["username"], user["email"]}
        return jsonify(user), 200

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


        # Check for existing email address
        if list(db.users.find_one()) != [] and db.users.find_one({"email": user['email']}):
            return jsonify({"failed": "Email address already in use"}), 400

        if request.form.get('password') != request.form.get('confirm_password'):
            return jsonify({"failed": "password are not the same"}), 400

        if db.users.insert_one(user):
            return redirect('/login')

        return jsonify({"failed": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        userFound = db.users.find_one({"email": request.form.get('email')})

        if userFound and bcrypt.hashpw(request.form.get('password')) == userFound['password']:
            return self.start_session(userFound)

        return jsonify({"failed": "Can't login due to wrong password or invalid email."}), 401