from flask import Flask, render_template, url_for, request, session, redirect, jsonify, flash
from flask_pymongo import MongoClient
from models import User
from forms import *
# from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'cse312 group project secret key'

# root: login page
@app.route('/', methods=["POST", "GET"])
def login_page():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return User.login()

    return render_template('login.html', form=login_form)

# # signup page
@app.route('/signup/', methods=["POST", "GET"])
def signup_page():
    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        #TODO: Save the information in the database and display a message that they can log in
        User().signup()
        flash("You successfully signed up!")
        return redirect(url_for("login_page"))

    return render_template('register.html', form=registration_form)

# game page
@app.route('/home/')
def home_page():
    return render_template('home.html')

# about page
@app.route("/about/")
def about_page():
    return render_template('about.html')

# profile page
@app.route('/profile/<userid>', methods=['GET'])
def profile_page(userid):
    if session.get("userid") != userid:
        return jsonify({"failed": "Login first."}), 401
    user = users.find_one({"_id": userid})
    return render_template('profile.html', user=user)

# leaderboard page
@app.route('/leaderboard/')
def leaderboard_page():
    board = list(rank.find())
    sample_board = [
        {"rank": "1", "username": "vwong", "wins": 10},
        {"rank": "2", "username": "poop", "wins": 2},
        {"rank": "3", "username": "valerie", "wins": 1}
    ]
    return render_template('leaderboard.html', boards=sample_board, title="Leaderboard")

# @app.route('/signup/', methods=['POST', "GET"])
# def signup_page():
#     if request.method == "POST":
#         return User().signup()
#     else:
#         return render_template("register.html")

# @app.route('/', methods=['POST', "GET"])
# def changeToSignup():
#   return redirect('/signup', code= 302)

# @app.route('/profile/signout')
# def signout():
#   return User().signout()

# @app.route('/profile/')
# def profileCheck():
#   if session.get("userid") == None:
#     return jsonify({"failed": "Login first."}), 401
#   return redirect('/profile/'+session.get("userid"))

# @app.route('/login', methods=['POST'])
# def login():
#   return User().login()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)