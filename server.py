from flask import Flask, render_template, url_for, session, redirect, jsonify, request, flash
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
    if "username" in session:
        join_room_form = JoinRoom()
        return render_template('lobby.html', form=join_room_form, username=session["username"])
    else:
        return redirect(url_for("login_page"))

# TODO
# Waiting for another player page
@app.route("/waiting_room/", methods=["GET"])
def waiting_page():
    username = session["username"]
    for room in players:
        if players[room] == username:
            room_id = room
    return render_template("waiting_room.html", username = username, room_id = room_id)

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
  if session.get("username") == None:
    return jsonify({"failed": "Login first to view profiles."}), 401

  return redirect('/profile/'+session.get("username"))

# any user's page
@app.route('/profile/<string:username>', methods=['GET'])
def profile_page(username):
    user = users.find_one({"username": username})
    user_board = users.find({}).sort("wins", -1)
    sorted_user_board = [user for user in user_board]
    user_rank = sorted_user_board.index(user)
    if user:
        editUsernameForm = editUserForm()
        return render_template('profile.html', form=editUsernameForm, user=user, username=session.get('username') , rank=user_rank)
    else:
        return jsonify({"failed": "User can not be found"}), 401

@app.route('/profile/<string:username>', methods=['POST'])
def edit_username(username):
    if session.get("username") != username:
        return jsonify({"failed": "In order to change this account's username, please login."}), 401

    newUsername = request.form.get('newUsername')

    is_avialable_name = users.find_one({"username": newUsername}) == None
    if is_avialable_name == False:
        flash("Username address already in use")
        return redirect('/profile/'+session.get("username"))
 
    users.find_one_and_update({"username": session.get("username")}, {"$set": {'username': newUsername}})
    session["username"] = newUsername
    return redirect('/profile/'+newUsername)

# leaderboard page
@app.route('/leaderboard/')
def leaderboard_page():
    # board = list(rank.find())
    user_board = users.find({}).sort("wins", -1)
    return render_template('leaderboard.html', boards=user_board, title="Leaderboard")


########################################################################################

# WEBSOCKET ROUTES

@app.route('/create_room', methods=["POST"])
def enter_waiting_room():
    return redirect(url_for("waiting_page"))

@socketio.on('create_room')
def create_room(data):
    print(f"The received data is: {data}")
    room_code = create_random_string(len = 4)
    print(f"The room code is: {room_code}")
    join_room(room_code)
    players[room_code] = data["username"]
    socketio.emit('new_game', {'room_id': room_code})
    print(f"The items in players is: {players.items()}")
    print(f"The room {room_code} has been created ")

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