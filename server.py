from flask import Flask, render_template, url_for, request, session, redirect, jsonify, flash
from models import User
from database import users
from forms import *

app = Flask(__name__)
app.secret_key = b'cse312 group project secret key' #TODO: Make an env file, store secret key in there and read secret key there 

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
    if session.get("userid") != None:
        user = users.find_one({"_id": session.get("userid")})
        return render_template('home.html', user=user)
    else:
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
  if session.get("username") == None:
    return jsonify({"failed": "Login first to view profiles."}), 401
  return redirect('/profile/'+session.get("username"))

#TODO: A user should be able to see another user's information, just not edit it
# any user's page
# change to view all users by username but edit only with session login
@app.route('/profile/<string:username>', methods=['GET'])
def profile_page(username):
    user = users.find_one({"username": username})
    if user:
        return render_template('profile.html', user=user, username=session.get('username') , rank="Not on list")
    else:
        return jsonify({"failed": "User can not be found"}), 401

@app.route('/profile/<string:username>', methods=['POST'])
def edit_username(username):
    if session.get("username") != username:
        return jsonify({"failed": "In order to change this account's username, please login."}), 401

    newUsername = request.form['newUsername']

    is_avialable_name = users.find_one({"username": session.get('username')}) == None
    if is_avialable_name == False:
        flash("Username address already in use")
        return redirect('/profile/'+session.get("username"))

    users.update_one({"username": session.get("username")}, {"$set": {'username': newUsername}})
    session["username"] = newUsername
    return redirect('/profile/'+newUsername)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)