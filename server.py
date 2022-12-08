from flask import Flask, render_template, url_for, session, redirect, jsonify, request
from models import User
from database import users
from forms import *
import random
import string

from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__)
app.secret_key = b'cse312 group project secret key' #TODO: Make an env file, store secret key in there and read secret key there 
socketio = SocketIO(app, cors_allowed_origins='*')

# TODO
# Socket global variables
players = {}
choice1 = ""
choice2 = ""

# Creates a random string in capital letters of length len
def create_random_string(len: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase, k=len))

# root: login page
@app.route('/', methods=["POST", "GET"])
def login_page():
    if "username" in session:
        return redirect(url_for("lobby_page"))
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

# lobby page
@app.route("/lobby/", methods = ["GET"])
def lobby_page():
    join_room_form = JoinRoom()
    return render_template('lobby.html', form=join_room_form)

# Waiting for another player page
@app.route("/waiting_room/", methods=["GET"])
def waiting_page():
    return render_template("waiting_room.html", username = session["username"])

# game page
@app.route('/game/')
def home_page():
    if session.get("userid") != None:
        user = users.find_one({"_id": session.get("userid")})
        return render_template('game.html', user=user)
    else:
        return render_template('game.html')

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

########################################################################################

# WEBSOCKET ROUTES

#TODO: Neeed to fix why the waiting page isnt being rendered
@socketio.on('create_room')
def create_room(data):
    room_code = create_random_string(len = 4)
    print(f"The room code is: {room_code}")
    join_room(room_code)
    players[room_code] = data["name"]
    socketio.emit('new_game', {'room_id': room_code})
    print(f"The room {room_code} has been created ")
    return redirect(url_for("waiting_page"))

#TODO
@socketio.on('join')
def create_game(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data["room"] + " room"}, to=data["room"]) #because we are using send, this will be sent to the "messages" event bucket on the client side

@socketio.on("leave")
def leave(data):
    leave_room(data["room"])
    send({'msg': data["username"] + " has left the " + data["room"] + " room"}, to=data["room"])

#########################################################################################

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080, debug=True)
    socketio.run(app, host="0.0.0.0", port=8080, debug=True, allow_unsafe_werkzeug=True)