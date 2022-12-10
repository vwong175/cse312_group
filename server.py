from flask import Flask, render_template, url_for, session, redirect, jsonify, request, flash
from models import User
from database import users
from forms import *
import random
import string
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import html
app = Flask(__name__)
app.secret_key = b'cse312 group project secret key' #TODO: Make an env file, store secret key in there and read secret key there 
socketio = SocketIO(app, cors_allowed_origins='*')


# Socket global variables
players = {}
choice = {'choice1':'','choice2':''}

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
        return render_template('lobby.html', form=join_room_form, username= html.escape(session["username"]))
    else:
        return redirect(url_for("login_page"))
        
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
    user_rank = sorted_user_board.index(user) + 1
    if user and 'username' in session:
        editUsernameForm = editUserForm()
        return render_template('profile.html', form=editUsernameForm, user=user, username= html.escape(session.get('username')) , rank=user_rank)
    elif user and 'username' not in session:
        editUsernameForm = editUserForm()
        return render_template('profile.html', form=editUsernameForm, user=user, username= "" , rank=user_rank)
    else:
        return jsonify({"failed": "User can not be found"}), 401

@app.route('/profile/<string:username>', methods=['POST'])
def edit_username(username):
    if session.get("username") != username:
        return jsonify({"failed": "In order to change this account's username, please login."}), 401

    newUsername = request.form.get('newUsername')

    is_avialable_name = users.find_one({"username": newUsername}) == None
    is_valid_name = '/' not in newUsername
    if not is_avialable_name:
        flash("Username already in use")
        return redirect('/profile/'+session.get("username"))
    if not is_valid_name:
        flash("Username cannot contain '/' !")
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

@socketio.on('create_room')
def create_room(data):
    room_code = create_random_string(len = 4)
    join_room(room_code)
    players[room_code] = data["username"]
    socketio.emit('new_game', {'room_id': room_code}, room=room_code)

@socketio.on('join_game')
def join_game(data):
    join_room(data['room_id'])
    socketio.emit('user2_joined', {'user2': data['username'], 'user1':players[data['room_id']]}, room=data['room_id'])

@socketio.on('leave_room')
def leave_game(data):
    socketio.emit('leave',{'username':data['username']}, room=data['room_id'])
    leave_room(data['room_id'])

@socketio.on('show_game_user_1')
def show_game_user_1():
    socketio.emit('show_game_user_1')

@socketio.on('player1_choice')
def player1_choice(data):
    choice['choice1'] = data['choice']
    choice1 = choice['choice1']
    choice2 = choice['choice2']
    result = ''
    if choice2 != '':
        if choice1 == choice2:
            result = 'TIE'
        elif choice1 == 'rock':
            if choice2 == 'scissor':
                result = 'player1_win'
            else:
                result = 'player2_win'
        elif choice1 == 'scissor':
            if choice2 == 'paper':
                result = 'player1_win'
            else:
                result = 'player2_win'
        else:
            if choice2 == 'rock':
                result = 'player1_win'
            else:
                result = 'player2_win'
        if result == 'player1_win':
            user_wins =  users.find_one({"username": data['player1']})['wins']
            users.find_one_and_update({"username": data['player1']}, {"$set": {'wins': user_wins + 1}})
        elif result == 'player2_win':
            user_wins =  users.find_one({"username": data['player2']})['wins']
            users.find_one_and_update({"username": data['player2']}, {"$set": {'wins': user_wins + 1}})
        socketio.emit('result', {'result':result}, room=data['room_id'])
        choice['choice1'] = ''
        choice['choice2'] = ''
    else:
        socketio.emit('wait', {'person_waiting':data['player1']}, room=data['room_id'])


@socketio.on('player2_choice')
def player2_choice(data):
    choice['choice2'] = data['choice']
    choice1 = choice['choice1']
    choice2 = choice['choice2']
    if choice1 != '':
        if choice1 == choice2:
            result = 'TIE'
        elif choice1 == 'rock':
            if choice2 == 'scissor':
                result = 'player1_win'
            else:
                result = 'player2_win'
        elif choice1 == 'scissor':
            if choice2 == 'paper':
                result = 'player1_win'
            else:
                result = 'player2_win'
        else:
            if choice2 == 'rock':
                result = 'player1_win'
            else:
                result = 'player2_win'
        if result == 'player1_win':
            user_wins =  users.find_one({"username": data['player1']})['wins']
            users.find_one_and_update({"username": data['player1']}, {"$set": {'wins': user_wins + 1}})
        elif result == 'player2_win':
            user_wins =  users.find_one({"username": data['player2']})['wins']
            users.find_one_and_update({"username": data['player2']}, {"$set": {'wins': user_wins + 1}})
        socketio.emit('result', {'result':result}, room=data['room_id'])
        choice['choice1'] = ''
        choice['choice2'] = ''
    else:
        socketio.emit('wait', {'person_waiting':data['player2']}, room=data['room_id'])

#########################################################################################

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8080, debug=True)
    socketio.run(app, host="0.0.0.0", port=8080, debug=True, allow_unsafe_werkzeug=True)
