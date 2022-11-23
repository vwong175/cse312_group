from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import MongoClient

from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'cse312 group project secret key'

client = MongoClient('localhost', 27017) #Connect to the hostname 'mongo' as defined in the docker compose file
db = client["userInfo"]
users = db["users"]
# rank in {"username",rank#} format
rank = db["rank"]


import routes

# root: login page
@app.route('/')
def login_page():
    return render_template('login.html')

# game page
@app.route('/home/')
def home_page():
    return render_template('home.html')

# about page
@app.route("/about/")
def about_page():
    return render_template('about.html')

# signup page
@app.route('/signup/', methods=["POST", "GET"])
def signup_page():
    if request.method == "POST":
        #Save the information in the database and display a message that they can log in
        return redirect(url_for("login_page"))
    else:
        return render_template('register.html')

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
    return render_template('leaderboard.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)