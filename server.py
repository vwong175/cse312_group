from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import MongoClient #I think this is correct?
from flask_login import LoginManager

app = Flask(__name__)
client = MongoClient('mongo') #Connect to the hostname 'mongo' as defined in the docker compose file
db = client['r_p_s']    #Select the database


#Collections
users = db['users']

@app.route('/', methods=["GET"])
def redirect_page():
    return redirect(url_for('register_page'))

@app.route('/login', methods=["GET"])
def login_page():
    return render_template('login.html')

@app.route('/register', methods=["GET"]) 
def register_page():
    return render_template('register.html')

@app.route('/home', methods=["GET"])
def home_page():
    return render_template('home.html')

@app.route('/leaderboard', methods=["GET"])
def leaderboard_page():
    return render_template('leaderboard.html')

class User():
    def __init__(self):
        self.username = 'test'
        self.wins = 1
        self.played = 1
@app.route('/profile', methods=["GET"])
def profile_page():
    return render_template('profile.html', user= User(), rank=1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True) #keep as 8080?