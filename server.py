from flask import Flask, render_template, url_for, request, session, redirect, jsonify, flash
from models import User
from database import users
from forms import *
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.secret_key = b'cse312 group project secret key' #TODO: Make an env file, store secret key in there and read secret key there 
socketio = SocketIO(app)

# root: login page
@app.route('/', methods=["POST", "GET"])
def login_page():
    if "username" in session:
        return redirect(url_for("home_page"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return User().login()
    return render_template('login.html', form=login_form)

# signup page
@app.route('/signup/', methods=["POST", "GET"])
def signup_page():
    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        return User().signup()
        
    return render_template('register.html', form=registration_form)

# game page
@app.route('/home/')
def home_page():
    return render_template('home.html')

# about page
@app.route("/about/")
def about_page():
    return render_template('about.html')

# signout page
@app.route("/profile/signout")
def signout_page():
    return User().signout()

# a user's profile page
@app.route("/profile/")
def profileCheck():
  if session.get("userid") == None:
    return jsonify({"failed": "Login first."}), 401
  return redirect('/profile/'+session.get("userid"))

#TODO: A user should be able to see another user's information, just not edit it
# any user's profile page
@app.route('/profile/<string:userid>', methods=['GET'])
def profile_page(userid):
    if session.get("userid") != userid:
        return jsonify({"failed": "Login first."}), 401
    user = users.find_one({"_id": userid})
    return render_template('profile.html', user=user)

# leaderboard page
@app.route('/leaderboard/')
def leaderboard_page():
    # board = list(rank.find())
    sample_board = [
        {"rank": "1", "username": "vwong", "wins": 10},
        {"rank": "2", "username": "poop", "wins": 2},
        {"rank": "3", "username": "valerie", "wins": 1}
    ]
    return render_template('leaderboard.html', boards=sample_board, title="Leaderboard")

@socketio.on('message')
def message(data):
    print(f"\r\n{data}\r\n")
    send(data)
if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0", port=8080, debug=True, allow_unsafe_werkzeug=True)