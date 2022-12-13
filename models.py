import bcrypt
from flask import Flask, jsonify, request, session, redirect, url_for, flash
from database import users
import uuid

class User:

    def start_session(self, user):
        session['logged_in'] = True
        session['userid'] = user["_id"]
        session["username"] = user["username"]
        return redirect('/profile/'+user["username"])

    def signup(self):
        salt = bcrypt.gensalt()

        #Usernames that contain '/' causes a bug, need to add a check for that
        is_valid_username = '/' not in request.form.get('username')
        if not is_valid_username:
            flash("Usernames cannot contain '/' !")
            return redirect(url_for('signup_page'))
        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "salt": salt,
            "password": bcrypt.hashpw(request.form.get('password').encode(), salt),
            "wins": 0,
            "played": 0
        }


        if len(list(users.find({}))) > 0:
            is_avialable_email = users.find_one({"email": user['email']}) == None
            is_avialable_name = users.find_one({"username": user['username']}) == None

            # Check for existing email address
            if is_avialable_email == False:
                flash("Email address already in use")
                return redirect(url_for('signup_page'))

            if is_avialable_name == False:
                flash("Username already in use")
                return redirect(url_for('signup_page'))

        if request.form.get('password') != request.form.get('confirm_password'):
            flash("password are not matched")
            return redirect(url_for('signup_page'))


        #TODO - Most definetly want to take a look at this one more time
        users.insert_one(user)
        print(list(users.find()))
        return redirect(url_for('login_page'))

    def signout(self):
        session.clear()
        flash("Sucessfully signed out!")
        return redirect('/')

    def login(self):

        if len(list(users.find({}))) > 0 :
            userFound: dict = users.find_one({"email": request.form.get('email')})

            if userFound and bcrypt.hashpw(request.form.get('password').encode(),userFound['salt']) == userFound['password']:
                return self.start_session(userFound)
        flash("Can't login due to wrong password or invalid email.")
        return redirect('/')